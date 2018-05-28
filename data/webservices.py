from community.git import get_org_name


def webservices_url(api_path):
    """
    Get API url for the webservices data.

    :param api_path: a string representing the API end_point
    :return: a url for the webservices data
    """
    webservices_path = 'webservices.' + get_org_name() + '.io/'
    url = ('https://rawgit.com/' + 'sks444/' + webservices_path +
           'master/' + api_path + '.json')
    return url
