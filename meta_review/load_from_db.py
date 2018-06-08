import logging

from meta_review.models import Participant, Comment, Reaction


def load_all(participants, comments, reactions):
    """
    Load all meta-review related data to memory.
    """
    load_participants(participants)
    load_comments(participants, comments)
    load_reactions(participants, comments, reactions)


def load_participants(participants):
    """
    Load participants into memory.

    a) create Participant objects if not exist in database
       fetch history data if exist in database and also in memory
    b) fetch history data if exist in database but not in memory yet
    """
    logger = logging.getLogger(__name__)
    logger.info('get or create participants')
    created_cnt = 0
    existing_cnt = 0
    load_cnt = 0
    # There are lots of participants and we'd better use bulk_create
    # to accelerate deploy process
    old_participants = Participant.objects.all()
    old_participants_set = set()
    for old_participant in old_participants:
        old_participants_set.add(old_participant.login)

    new_participants = []
    for participant in participants.values():
        # if it is an old participant, we skip it
        if participant['login'] in old_participants_set:
            logger.debug('participant %s exists' % participant['login'])
            existing_cnt += 1
        else:
            logger.debug('participant %s is new' % participant['login'])
            new_participants.append(
                Participant(login=participant['login']))
            created_cnt += 1

    # use bulk create to speed up create process
    Participant.objects.bulk_create(new_participants)

    # load all participants again (old + new)
    all_participants = Participant.objects.all()

    for p in all_participants:
        if participants.get(p.login):
            # participants recently active
            participant = participants[p.login]
            p.name = participant['name']
        else:
            # participants recently inactive
            # they are not in self.participants, but their ranks need update
            load_cnt += 1
        # save into memory
        participants[p.login] = p

    logger.info('newly created participants: %d '
                'existing active participants: %d '
                'existing inactive participants: %d'
                % (created_cnt, existing_cnt, load_cnt))

    logger.info('load participants into memory done, '
                'total number = %d'
                % (created_cnt + existing_cnt + load_cnt))


def load_comments(participants, comments):
    """
    Load reviews into memory.

    a) create Review objects if not exist in database
    b) fetch history data if exist in database
    """
    logger = logging.getLogger(__name__)
    logger.info('get or create reviews')
    created_cnt = 0
    existing_cnt = 0
    # There are lots of comments and we have to use bulk_create
    # to accelerate deploy process
    old_comments = Comment.objects.all()
    old_comments_set = set()
    for old_comment in old_comments:
        old_comments_set.add(old_comment.id)

    new_comments = []
    for comment in comments.values():
        # if it is an old comment, we skip it
        if comment['id'] in old_comments_set:
            logger.debug('review comment %s exists' % comment['id'])
            existing_cnt += 1
        else:
            logger.debug('review comment %s is new' % comment['id'])
            new_comments.append(
                Comment(id=comment['id']))
            created_cnt += 1

    # use bulk create to speed up create process
    Comment.objects.bulk_create(new_comments)

    # load all comments again (old + new)
    all_comments = Comment.objects.all()

    for c in all_comments:
        if not comments.get(c.id):
            # no need to load history comments
            continue
        comment = comments[c.id]
        c.body = comment['bodyText']
        c.diff = comment['diffHunk']
        c.created_at = comment['createdAt']
        c.last_edited_at = comment['lastEditedAt']
        login = comment['author']['login']
        if login:
            c.author = participants[login]

        # save into memory
        comments[c.id] = c

    logger.info('number of newly created comment objects: %d '
                'number of existing comment objects: %d'
                % (created_cnt, existing_cnt))


def load_reactions(participants, comments, reactions):
    """
    Load reactions into memory.

    a) create Reaction objects if not exist in database
    b) fetch history data if exist in database
    """
    logger = logging.getLogger(__name__)
    logger.info('get or create reactions')
    created_cnt = 0
    existing_cnt = 0

    # There are lots of reactions and we have to use bulk_create
    # to accelerate deploy process
    old_reactions = Reaction.objects.all()
    old_reactions_set = set()
    for old_reaction in old_reactions:
        old_reactions_set.add(old_reaction.id)

    new_reactions = []
    for reaction in reactions.values():
        # if it is an old reaction, we skip it
        if reaction['id'] in old_reactions_set:
            logger.debug('reaction %s exists' % reaction['id'])
            existing_cnt += 1
        else:
            logger.debug('reaction %s is new' % reaction['id'])
            new_reactions.append(
                Reaction(id=reaction['id']))
            created_cnt += 1

    # use bulk create to speed up create process
    Reaction.objects.bulk_create(new_reactions)

    # load all reactions again (old + new)
    all_reactions = Reaction.objects.all()

    for r in all_reactions:
        if not reactions.get(r.id):
            # no need to load history reactions
            continue
        reaction = reactions[r.id]
        r.created_at = reaction['createdAt']
        r.content = reaction['content']
        giver_login = reaction['user']['login']
        if giver_login:
            r.giver = participants[giver_login]
        receiver_login = reaction['receiver']['login']
        if receiver_login:
            r.receiver = participants[receiver_login]
        comment_id = reaction['comment_id']
        r.review = comments[comment_id]

        # save into memory
        reactions[r.id] = r

    logger.info('number of newly created reaction objects: %d '
                'number of existing reaction objects: %d'
                % (created_cnt, existing_cnt))
