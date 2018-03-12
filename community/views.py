from django.http import HttpResponse

from .git import (
    get_deploy_url,
    get_org_name,
    get_owner,
    get_upstream_deploy_url,
)


def info(request):
    data = {
        'Org name': get_org_name(),
        'Owner': get_owner(),
        'Deploy URL': get_deploy_url(),
    }
    try:
        upstream_deploy_url = get_upstream_deploy_url()
        data['Upstream deploy URL'] = upstream_deploy_url
    except RuntimeError:
        data['Upstream deploy URL'] = 'Not found'

    s = '\n'.join(name + ': ' + value
                  for name, value in data.items())
    return HttpResponse(s)
