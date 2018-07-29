def data_checker(data):
    """
    When there is only one item on the OpenHub API
    page, the return type of the data is 'dict', containing
    the details of that single item, which should be converted
    into the 'list' of 'dict'. As the return type of the methods
    'get_affiliated_committers_data', 'get_outside_committers_data',
    'get_outside_projects_data', and 'get_portfolio_projects_data'
    is a list of dict.

    This method checks if the type of the data is dict,
    if yes, then it convert the data into a list of dict.

    This method also verify that the contents of the dict
    is the details of a single item, by checking the length of
    the dict, which should always be '5'. As a dict contains
    only '5' keys(details) for a single item.
    """
    if isinstance(data, dict):
        assert len(data) == 5
        data = [data]
    return data
