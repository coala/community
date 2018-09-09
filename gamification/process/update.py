import logging

from data.models import (
    MergeRequest,
    Issue,
)
from data.newcomers import active_newcomers
from gamification.process.activity_points import (
    get_activity_with_points
)
from gamification.labels import NEGATIVE_POINT_LABELS
from gamification.data.points import MERGE_REQUEST_CLOSED_WITHOUT_MERGE
from gamification.models import Participant
from meta_review.models import Reaction, Participant as meta_review_participants


def get_mr_objects():
    """
    Get mrs objects saved in the database.

    :return: a queryset of mr objects.
    """
    mrs = MergeRequest.objects.all()
    return mrs


def update_participants_data_with_mr(mr):
    """
    Update participants data based on mr.

    This method updates the total score earned by the
    participant based on the activities performed,
    and then update the current level based on the
    total score.

    This method first check if the mr is merged or not,
    if it's merged, then it's get a activity and points based
    on the labels on mr and update the participant data who
    opened this mr.

    Further it gets all the issues that mr is closing then get the
    points and activity based on the labels on the issue and update
    the participant data who opened that issue.
    """
    logger = logging.getLogger(__name__)

    # Get the participant who opened this mr
    mr_author = Participant.objects.get(username=mr.author)
    mr_performed_at = mr.created_at
    mr_updated_at = mr.updated_at

    if mr.state == 'merged':
        mr_labels = mr.labels.values('name')

        # Get activity and points based on labels on the mr
        mr_points, mr_activity_string = get_activity_with_points(
            'merge_request', mr_labels)

        # Update participant data
        mr_author.add_points(mr_points,
                             mr_activity_string,
                             mr_performed_at,
                             mr_updated_at,
                             )
        # Get all the issues this mr is closing
        try:
            issues = mr.get_closes_issues_object()
        except Exception as ex:
            logger.error(ex)
            return
        for issue in issues:
            issue_labels = issue.labels.values('name')
            issue_performed_at = issue.created_at
            issue_updated_at = issue.updated_at
            # Get activity and points based on the labels on the issue
            issue_points, issue_activity_string = get_activity_with_points(
                'issue', issue_labels)
            if issue.author == mr.author:
                issue_author = mr_author
            else:
                issue_author = Participant.objects.get(username=issue.author)
            # Update participant data who opened the issue
            issue_author.add_points(issue_points,
                                    issue_activity_string,
                                    issue_performed_at,
                                    issue_updated_at,
                                    )

    elif mr.state == 'closed':
        mr_points = MERGE_REQUEST_CLOSED_WITHOUT_MERGE
        mr_activity_string = 'Merge request was closed without merge'
        mr_author.deduct_points(mr_points,
                                mr_activity_string,
                                mr_performed_at,
                                mr_updated_at,
                                )


def get_issue_objects():
    """
    Get issue objects saved in the database.

    :return: a queryset of issue objects.
    """
    issues = Issue.objects.all()
    return issues


def update_participants_data_with_issue(issue):
    """
    Update participant data based on issue.

    This method only run for the issues which has
    'status/invalid' or 'status/duplicate' or both the
    labels. If both the labels are present in the issue
    issue_activity return by 'get_activity_with_points' would
    be 'Create a status/invalid issue' and the points would be
    '-5'.
    """
    labels = issue.labels.values('name')
    labels_list = [label['name'] for label in labels]
    if any(x in labels_list for x in NEGATIVE_POINT_LABELS):
        issue_author = Participant.objects.get(username=issue.author)
        issue_points, issue_activity = get_activity_with_points('issue', labels)
        issue_performed_at = issue.created_at
        issue_updated_at = issue.updated_at
        issue_author.deduct_points(issue_points,
                                   issue_activity,
                                   issue_performed_at,
                                   issue_updated_at,
                                   )
        issue_author.save()


def get_participant_objects():
    participants = Participant.objects.all()
    return participants


def get_meta_review_participant_objects():
    return meta_review_participants.objects.all()


meta_review_completed_list = []


def update_participants_data_with_meta_review(meta_review_participant):
    """
    Update participants based on meta-review

    This method updates every participant based on the meta-review
    received or given. If the  meta-review participant is
    in the active newcomers list then it will check if the meta-review
    is complete or not and update the activity accordingly.
    """
    active_newcomers_list = active_newcomers()
    if (meta_review_participant.login in active_newcomers_list and
            meta_review_participant.login not in meta_review_completed_list):
        # Get the corresponding gamification participant
        gamification_participant = Participant.objects.get(
            username=meta_review_participant.login)
        reaction = Reaction.objects.get(id=meta_review_participant.login)
        if (meta_review_participant.pos_in > 0 or
                meta_review_participant.pos_out > 0 or
                meta_review_participant.neg_in > 0 or
                meta_review_participant.neg_out > 0):
            # Add a meta-review activity to the participant
            activity = 'Did a meta-review or received a meta-review'
            created_at = reaction.created_at
            updated_at = None
            gamification_participant.add_activity(0, activity, created_at,
                                                  updated_at)
            meta_review_completed_list.append(meta_review_participant.login)
            logger = logging.getLogger(__name__)
            logger.info(meta_review_participant.login,
                        ' has completed the meta-review activity')


def award_badges(participant):
    activities = participant.activities.values('name')
    participant.add_badges(activities)
