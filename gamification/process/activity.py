def get_activity(activity_type, labels):
    """
    Get an activity based on the labels on issues or mrs.

    :param activity_type: a string representing the type of the
                          activity. e.g. issue or merge_request.
    :param labels:        a list of sorted labels.
    :return:              a touple of points and activity string.
    """
    activity_starts_with = None
    if activity_type == 'issue':
        activity_starts_with = 'Created a '
    elif activity_type == 'merge_request':
        activity_starts_with = 'Solved a '
    else:
        raise ValueError('Activity type is not defined.')
    activity = activity_starts_with + ' '.join(labels) + ' issue'
    return activity
