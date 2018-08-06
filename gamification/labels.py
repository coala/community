from gamification.data.points import ISSUE_POINTS_DICT

POSITIVE_POINT_LABELS = [
    label for label, score in ISSUE_POINTS_DICT.items() if score > 0]
NEGATIVE_POINT_LABELS = [
    label for label, score in ISSUE_POINTS_DICT.items() if score < 0]


def get_sorted_labels(labels):
    """
    Get sorted labels.

    :param labels: a QuerySet dict containing the 'name'
                   as key and 'name of the label' as value.
    :return:       a list of sorted labels.
    """
    labels_list = [label['name'] for label in labels]

    modified_labels_list = []
    if any(x in labels_list for x in NEGATIVE_POINT_LABELS):
        for label in labels_list:
            if label in NEGATIVE_POINT_LABELS:
                modified_labels_list.append(label)
            if len(modified_labels_list) == 2:
                modified_labels_list.remove('status/duplicate')
    else:
        for label in labels_list:
            if label in POSITIVE_POINT_LABELS:
                modified_labels_list.append(label)

    # Sorting the labels to get consistent activity
    modified_labels_list.sort()
    return modified_labels_list
