from gamification.process.activity import get_activity
from gamification.points import get_total_points
from gamification.labels import get_sorted_labels


def get_activity_with_points(activity_type, labels):
    """
    Get an activity with points based on the labels
    on the issues or mrs.

    :param activity_type: a string representing the type of the
                          activity. e.g. issue or merge_request.
    :param labels:        a QuerySet dict containing the 'name'
                          as key and 'name of the label' as value.
    :return:              a tuple of points and activity string.
    """
    labels = get_sorted_labels(labels)
    points = get_total_points(activity_type, labels)
    activity = get_activity(activity_type, labels)
    return points, activity
