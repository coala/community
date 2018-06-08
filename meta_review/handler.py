from dateutil import parser
import json
import logging
import os

from django.utils import timezone

from meta_review.dump_to_db import dump_all
from meta_review.load_from_db import load_all
from meta_review.models import Participant


def parse_time(time):
    """
    Parse string to datetime.

    :param time: a string represents time, e.g. 2018-05-09T11:19:26Z
    :return: an offset-aware datetime object
    """
    if time is None:
        return None

    return parser.parse(time)


class MetaReviewHandler:
    """
    Handle meta-review system.

    This is the class responsible for scraping provided information (reviews,
    reactions), processing them and dumping into Django database.
    """

    # coefficients of the scoring formula
    BONUS_GIVE_POS = 0.05
    BONUS_GIVE_NEG = 0.2

    # point offset due to edited review after meta-review
    LATE_EDIT_SCORE_OFFSET = 0.5

    def __init__(self, content, date):
        """
        Construct a new ``MetaReviewHandler``.

        :param content: Parsed JSON data
        :param date: The update date
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('this package is alive')

        self.date = date

        # save comments in memory
        self.comments = dict()
        for issue in content:
            issue = issue['issue']
            if not issue.get('pullRequest'):
                continue
            for comment in issue['pullRequest']['comments']:
                if not comment.get('reactions') or not comment['reactions']:
                    # there is no need to store comments which have
                    # not yet been meta-reviewed
                    continue
                # parse time
                comment['createdAt'] = parse_time(comment['createdAt'])
                comment['lastEditedAt'] = parse_time(comment['lastEditedAt'])
                self.comments[comment['id']] = comment

        # save reactions in memory
        self.reactions = dict()
        for comment in self.comments.values():
            for reaction_data in comment['reactions']:
                # record receiver
                reaction_data['receiver'] = {
                    'login': comment['author']['login']
                }
                # record comment id
                reaction_data['comment_id'] = comment['id']
                # parse time
                reaction_data['createdAt'] = parse_time(
                    reaction_data['createdAt'])
                self.reactions[reaction_data['id']] = reaction_data

        # save participants in memory
        self.participants = dict()
        for comment in self.comments.values():
            # get author of each comment
            author = comment['author']

            # skip if user does not exist
            # this happens when account is deleted from GitHub
            if author['login']:
                self.participants[author['login']] = author

            if not comment.get('reactions'):
                continue
            for reaction in comment['reactions']:
                # get user of each reaction
                user = reaction['user']

                # skip if user does not exist
                if user['login']:
                    self.participants[user['login']] = user

    def handle(self):
        """
        Scrape data, process and store in database.
        """
        is_first_deploy = self._is_first_deploy()

        load_all(self.participants, self.comments, self.reactions)
        dump_all(self.participants, self.comments, self.reactions)

        self._update_scores()
        self._update_weight_factors()

        if is_first_deploy:
            # dump first to make use of reverse query
            dump_all(self.participants, self.comments, self.reactions)
            self._recalculate_score()

        self._apply_negative_scores()
        self._update_time()

        # dump first to make use of built-in sort method
        dump_all(self.participants, self.comments, self.reactions)
        self._update_rankings()

        dump_all(self.participants, self.comments, self.reactions)

        self.logger.info('Meta Review System finishes.')

    def get_comments_modified_after_meta_review(self):
        """
        Generator for comments modified after meta-review.

        Yield comments which are modified after they have been meta-reviewed.
        """
        for comment in self.comments.values():
            last_edited_at = comment.last_edited_at
            author = comment.author

            # skip if author does not exist
            if not author:
                continue

            comment_modified_after_meta_review = False
            reactions = comment.reaction_set.all()

            # get reactions createdTime
            for reaction in reactions:
                if last_edited_at and last_edited_at > reaction.created_at:
                    comment_modified_after_meta_review = True
                    break

            if comment_modified_after_meta_review:
                self.logger.info('%s updates review comment after it has been '
                                 'meta-reviewed. Comment id: %s'
                                 % (author.login, comment.id))
                yield comment

    def _apply_negative_scores(self):
        """
        Give point offset to participants who did improper behavior.

        If an author updates his review comment after it has been
        meta-reviewed, he will be slightly punished.
        """
        for participant in self.participants.values():
            # give punished score back to the participant first,
            # as offset will be recalculated later
            participant.score += participant.offset
            participant.modified_comments_after_meta_review = 0
            participant.offset = 0

        for comment in self.get_comments_modified_after_meta_review():
            author = comment.author
            self.logger.info('%s has improper behavior'
                             '(edit comment after it has been '
                             'meta-reviewed) on comment %s. %.2f '
                             'point deducted.'
                             % (author.login, comment.id,
                                self.LATE_EDIT_SCORE_OFFSET))
            author.score -= self.LATE_EDIT_SCORE_OFFSET
            author.modified_comments_after_meta_review += 1
            author.offset += self.LATE_EDIT_SCORE_OFFSET

    def _update_time(self):
        """
        Update last_active_at attribute of each participant.

        Note this does not accurately reflect the last time they were
        active in the community.

        First, it relies on the accuracy of issues.json fetched from
        gh-board repo.

        Second, this field should instead be interpreted as 'the last
        time the participant had impact on the meta-review system'. This
        is the last time among three things: the last time they created/edited
        a comment, the last time they did a meta-review, the last time
        their review received a meta-review.
        """
        self.logger.info('start updating last active time of all participants')

        for participant in self.participants.values():
            old_active_time = participant.last_active_at

            # check last time they created/edited a comment
            for comment in participant.comment_set.all():
                if participant.last_active_at is None:
                    participant.last_active_at = comment.created_at
                if comment.created_at > participant.last_active_at:
                    participant.last_active_at = comment.created_at
                if (comment.last_edited_at and
                        comment.last_edited_at > participant.last_active_at):
                    participant.last_active_at = comment.last_edited_at

            # check last time they did a meta-review
            for reaction in participant.give.all():
                if participant.last_active_at is None:
                    participant.last_active_at = reaction.created_at
                if reaction.created_at > participant.last_active_at:
                    participant.last_active_at = reaction.created_at

            # check last time they received a meta-review
            for reaction in participant.receive.all():
                if participant.last_active_at is None:
                    participant.last_active_at = reaction.created_at
                if reaction.created_at > participant.last_active_at:
                    participant.last_active_at = reaction.created_at

            if participant.last_active_at != old_active_time:
                self.logger.debug('%s last active time changed from %s to %s'
                                  % (participant.login, old_active_time,
                                     participant.last_active_at))

    @staticmethod
    def _is_first_deploy():
        """
        Check whether it is the first deploy.

        If the scoring system has not been run before, we need to calculate
        draft score first, and then weight factor. Finally we use that
        to recalculate score.

        :return: a bool indicates whether this is the first deploy.
        """
        # This query set is empty means it is the first deploy.
        return not Participant.objects.all()

    def _recalculate_score(self):
        """
        Recalculate score of each participant.

        Used only on first deploy. Based on the weight factor derived,
        recalculate score for all participants and comments.
        """
        self.logger.info('recalculate score of each participant')
        for comment in self.comments.values():
            comment.clear_score()

        for participant in self.participants.values():
            participant.clear_score()

        self._update_scores()
        self._update_weight_factors()

    def _update_scores(self):
        """
        Update score of each participant.

        Calculate and update score of each participant using
        the following formula:

        Define:

        P1 = total points (weighted) of THUMBS_UP a person gets for all
             reviews he did.
        P2 = total number of THUMBS_UP a person gives to other
             people for their reviews.
        N1 = total points (weighted) of THUMBS_DOWN a person gets for all
             reviews he did.
        N2 = total number of THUMBS_DOWN a person gives to other people for
             their reviews.

        Then final score, denote by S, is as follows:

        S = P1 - N1 + BONUS_GIVE_POS * P2 + BONUS_GIVE_NEG * N2

        where BONUS_GIVE_POS = 0.05, BONUS_GIVE_NEG = 0.2. One will get at
        least 0.1 point for a positive reaction they received, so we want
        BONUS_GIVE_POS to be smaller than that. BONUS_GIVE_NEG is larger
        because people are reluctant to give negative reactions.
        In all, bonus points (P2 and N2) aim to encourage people to do
        meta-reviews, but we don't want them to dominate.

        Also update score of each review comment.
        """
        self.logger.info('update scores of all participants')

        for participant in self.participants.values():
            # parameters to be used in the formula
            p1, p2, n1, n2 = 0, 0, 0, 0

            # number of positive/negative reactions received
            pos_cnt, neg_cnt = 0, 0

            time = participant.last_active_at
            # get reactions received
            if not time:
                reactions_in = participant.receive.all()
            else:
                reactions_in = participant.receive.filter(created_at__gt=time)
            for reaction in reactions_in:
                # get weight factor of the reaction giver
                weight_factor = reaction.giver.weight_factor
                if reaction.content.find('THUMBS_UP') != -1:
                    self.logger.debug('reaction received is %s, positive'
                                      % reaction.content)
                    p1 += weight_factor
                    pos_cnt += 1
                    # also update score of review comment
                    reaction.review.pos += 1
                    reaction.review.weighted_pos += weight_factor
                    reaction.review.score += weight_factor
                elif reaction.content.find('THUMBS_DOWN') != -1:
                    self.logger.debug('reaction received is %s, negative'
                                      % reaction.content)
                    n1 += weight_factor
                    neg_cnt += 1
                    # also update score of review comment
                    reaction.review.neg += 1
                    reaction.review.weighted_neg += weight_factor
                    reaction.review.score -= weight_factor
                else:
                    self.logger.debug('reaction received is %s, ignore'
                                      % reaction.content)

            # get reactions give away
            if not time:
                reactions_out = participant.give.all()
            else:
                reactions_out = participant.give.filter(created_at__gt=time)
            for reaction in reactions_out:
                if reaction.content.find('THUMBS_UP') != -1:
                    self.logger.debug('reaction give away is %s, positive'
                                      % reaction.content)
                    p2 += 1
                elif reaction.content.find('THUMBS_DOWN') != -1:
                    self.logger.debug('reaction give away is %s, negative'
                                      % reaction.content)
                    n2 += 1
                else:
                    self.logger.debug('reaction give away is %s, ignore'
                                      % reaction.content)

            # update information
            participant.pos_in += pos_cnt
            participant.weighted_pos_in += p1
            participant.pos_out += p2
            participant.neg_in += neg_cnt
            participant.weighted_neg_in += n1
            participant.neg_out += n2
            self.logger.debug('update %s info, pos_in += %d, '
                              'weighted_pos_in += %.3f, pos_out += %d, '
                              'neg_in += %d, weighted_neg_in += %.3f, '
                              'neg_out += %d'
                              % (participant.login, pos_cnt, p1, p2,
                                 neg_cnt, n1, n2))

            # update score
            s = p1 - n1 + self.BONUS_GIVE_POS * p2 + self.BONUS_GIVE_NEG * n2
            self.logger.debug('update %s score, before: %.3f, after: %.3f'
                              % (participant.login, participant.score,
                                 participant.score + s))
            participant.score += s

    def _update_rankings(self):
        """
        Update rankings.

        Calculate and update rankings based on scores by making
        use of Django built-in sorting method.
        """
        self.logger.info('update rankings of all participants')

        # make use of built-in order_by method to sort participants
        participants_all = Participant.objects.order_by('-score', '-pos_in')
        rank = 0
        last_score = -float('inf')
        for participant in participants_all:
            if rank == 0 or last_score != participant.score:
                rank += 1
                last_score = participant.score

            # update trend = rank (last time) - rank (this time)
            if participant.rank:
                if participant.trend:
                    self.logger.debug('update %s trend, before: %d, after: %d'
                                      % (participant.login, participant.trend,
                                         participant.rank - rank))
                else:
                    # if last time was the first time they get a rank, then
                    # they don't have trend last time
                    self.logger.debug('update %s trend, before: N/A, after: %d'
                                      % (participant.login,
                                         participant.rank - rank))
                participant.trend = participant.rank - rank
            else:
                self.logger.debug('%s has no rank before, thus no trend'
                                  % participant.login)

            # update rank
            if participant.rank:
                self.logger.debug('update %s rank, before: %d, after: %d'
                                  % (participant.login, participant.rank,
                                     rank))
            else:
                self.logger.debug('update %s rank, before: N/A, after: %d'
                                  % (participant.login, rank))
            participant.rank = rank

            # save in memory
            self.participants[participant.login] = participant

    def _update_weight_factors(self):
        """
        Update weight factor of each participant.

        Based on history data and the current iteration, recalculate weight
        factors (to be used in the next iteration).

        The higher score a person has, the more impacts he has, thus his
        meta-reviews are more valuable.

        For example, in a previous iteration, Alice got 2 marks, Bob got
        0.8 marks and Charlie got 10 marks. The calculation demo would
        be as follows:

        >>> c = [2, 0.8, 10]
        >>> max_score = float(max(c))
        >>> result = [i / max_score for i in c]
        >>> print(result)
        [0.2, 0.08, 1.0]
        >>> result_adjust = [i * 0.9 + 0.1 for i in result]  # adjust
        >>> result_rounded = [round(i, 3) for i in result_adjust]
        >>> print(result_rounded)
        [0.28, 0.172, 1.0]

        Anyone who gets negative marks from previous run will have weight
        factor of 0.

        To conclude, the weight factor is a float number ranging from 0 to 1.
        """
        max_score = 1.0
        # find max score
        for participant in self.participants.values():
            if participant.score > max_score:
                max_score = float(participant.score)

        # calculate weight factors
        for participant in self.participants.values():
            if participant.score < 0:
                participant.weight_factor = 0
            else:
                participant.weight_factor = participant.score / max_score
                participant.weight_factor *= 0.9
                participant.weight_factor += 0.1


def handle():
    """
    Handle meta-review system.

    Get issues.json first and then use MetaReviewHandler to process it.
    """
    logger = logging.getLogger(__name__)
    try:
        with open(os.path.join('_site', 'issues.json')) as f:
            parsed_json = json.load(f)
        handler = MetaReviewHandler(parsed_json['issues'], timezone.now())
        handler.handle()
    except Exception as ex:
        logger.error('load issues.json error: %s' % ex)
