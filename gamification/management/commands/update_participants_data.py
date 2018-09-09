import logging

from django.core.management.base import BaseCommand

from gamification.process.update import (
    get_mr_objects,
    update_participants_data_with_mr,
    get_issue_objects,
    update_participants_data_with_issue,
    get_participant_objects,
    award_badges,
    get_meta_review_participant_objects,
    update_participants_data_with_meta_review,
)


class Command(BaseCommand):
    help = 'Update participants data'

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        for mr in get_mr_objects():
            if not mr.labels.count():
                logger.warning(
                    'Merge request: %s has no labels.' % mr.url)
                continue
            update_participants_data_with_mr(mr)
        for issue in get_issue_objects():
            if not issue.labels.count():
                logger.warning(
                    'Issue: %s has no labels.' % issue.url)
                continue
            update_participants_data_with_issue(issue)
        for participant in get_participant_objects():
            award_badges(participant)
        for participant in get_meta_review_participant_objects():
            update_participants_data_with_meta_review(participant.login)
