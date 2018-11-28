from django.http import HttpResponse
from django.views.generic.base import TemplateView

from trav import Travis

from .git import (
    get_deploy_url,
    get_org_name,
    get_owner,
    get_upstream_deploy_url,
)


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isTravis'] = Travis.TRAVIS
        context['travisLink'] = Travis.TRAVIS_BUILD_WEB_URL

        print('Running on Travis: {}, build link: {}'.format(
            context['isTravis'],
            context['travisLink']))

        return context


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
