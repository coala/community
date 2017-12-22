from community.git import get_owner


def get_org_name(request):
    org_name = get_owner()
    return {'org_name': org_name}
