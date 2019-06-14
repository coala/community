import json

from django.views.generic import TemplateView

from community.views import get_header_and_footer
from gamification.models import Participant, Level, Badge


class GamificationResults(TemplateView):
    template_name = 'gamification.html'
    participants = Participant.objects.all()

    def get_users_username(self, users):
        """
        :param users: A Queryset, with a field username
        :return: A list of usernames
        """
        usernames = list()
        for user in users:
            usernames.append(user.username)
        return usernames

    def group_participants_by_score(self):
        """
        Divide the participants according to their scores. For example, if
        there are 10 contributors who have different scores and there are
        possibly 4 ranges i.e. score_gt 80, score_between (70,80),
        score_between (60,70) and score_lt 60. So, divide them and put them
        in their respective lists.
        :return: A Dict, with key as score_range and value a list of
        contributors username
        """
        scores = set()
        for contrib in self.participants:
            scores.add(contrib.score)

        scores = list(scores)
        scores.sort()

        try:
            min_score, max_score = scores[0], scores[-1]
        except IndexError:
            return dict()

        difference_bw_groups_score = int(max_score/5)
        score_ranges = [
            min_score + i * difference_bw_groups_score for i in range(6)
        ]
        score_ranges[-1] += max_score % 5

        grouped_participants = dict()
        for index, score in enumerate(score_ranges[1:]):
            begin_score, end_score = score_ranges[index], score

            filtered_participants = self.participants.filter(
                score__range=[begin_score, end_score]
            )

            if begin_score == min_score:
                grp_lvl = f'<{end_score}'
            elif end_score < max_score:
                grp_lvl = f'>={begin_score} and <{end_score}'
            else:
                grp_lvl = f'>={begin_score}'

            grouped_participants[grp_lvl] = json.dumps(
                self.get_users_username(filtered_participants)
            )
        return grouped_participants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['gamification_results'] = self.participants
        context['levels'] = Level.objects.all()
        context['badges'] = Badge.objects.all()
        context['grouped_participants'] = self.group_participants_by_score()

        return context
