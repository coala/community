from gamification.data.points import (
    ISSUE_POINTS_DICT,
    MR_POINTS_DICT,
)


def get_total_points(activity_type, labels):
    """
    Get total points.

    :param activity_type: a string representing the type of
                          the activity. e.g. issue or merge_request
    :param labels:        a list of sorted labels.
    :return:              a integer value representing the total points.
    """
    points = 0
    for label in labels:
        plus_points = 0
        if activity_type == 'issue':
            plus_points = ISSUE_POINTS_DICT.get(label, 0)
        elif activity_type == 'merge_request':
            plus_points = MR_POINTS_DICT.get(label, 0)
        else:
            raise ValueError('Activity type is not defined.')
        points = points + plus_points
    return points
