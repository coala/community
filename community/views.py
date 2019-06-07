import logging

import requests

from trav import Travis

from django.http import HttpResponse
from django.views.generic.base import TemplateView

from .git import (
    get_deploy_url,
    get_org_name,
    get_owner,
    get_upstream_deploy_url,
    get_remote_url
)
from data.models import Team
from gamification.models import Participant as GamificationParticipant
from meta_review.models import Participant as MetaReviewer


def initialize_org_context_details():
    org_name = get_org_name()
    org_details = {
        'name': org_name,
        'blog_url': f'https://blog.{org_name}.io/',
        'twitter_url': f'https://twitter.com/{org_name}_io/',
        'facebook_url': f'https://www.facebook.com/{org_name}Analyzer',
        'repo_url': get_remote_url().href,
        'docs': f'https://{org_name}.io/docs',
        'newcomer_docs': f'https://{org_name}.io/newcomer',
        'coc': f'https://{org_name}.io/coc',
        'logo_url': (f'https://api.{org_name}.io/en/latest/_static/images/'
                     f'{org_name}_logo.svg'),
        'gitter_chat': f'https://gitter.im/{org_name}/{org_name}/',
        'github_core_repo': f'https://github.com/{org_name}/{org_name}/',
        'licence_type': 'GNU AGPL v3.0'
    }
    return org_details


def get_header_and_footer(context):
    context['isTravis'] = Travis.TRAVIS
    context['travisLink'] = Travis.TRAVIS_BUILD_WEB_URL
    context['org'] = initialize_org_context_details()
    print('Running on Travis: {}, build link: {}'.format(context['isTravis'],
                                                         context['travisLink']
                                                         ))
    return context


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_team_details(self, org_name):
        teams = [
            f'{org_name} newcomers',
            f'{org_name} developers',
            f'{org_name} admins'
        ]
        team_details = {}
        for team_name in teams:
            team = Team.objects.get(name=team_name)
            contributors_count = team.contributors.count()
            team_details[
                team_name.replace(org_name, '').strip().capitalize()
            ] = contributors_count
        return team_details

    def get_quote_of_the_day(self):

        try:
            qod = requests.get('http://quotes.rest/qod?category=inspire')
            qod.raise_for_status()
        except requests.HTTPError as err:
            error_info = f'HTTPError while fetching Quote of the day! {err}'
            logging.error(error_info)
            return

        qod_data = qod.json()
        return {
            'quote': qod_data['contents']['quotes'][0]['quote'],
            'author': qod_data['contents']['quotes'][0]['author'],
        }

    def get_top_meta_review_users(self, count):
        participants = MetaReviewer.objects.all()[:count]
        return participants

    def get_top_gamification_users(self, count):
        return enumerate(GamificationParticipant.objects.all()[:count])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        org_name = context['org']['name']
        context['org']['team_details'] = dict(self.get_team_details(org_name))
        about_org = (f'{org_name} (always spelled with a lowercase c!) is one'
                     ' of the welcoming open-source organizations for'
                     f' newcomers. {org_name} stands for “COde AnaLysis'
                     ' Application” as it works well with animals and thus is'
                     ' well visualizable which makes it easy to memorize.'
                     f' {org_name} provides a unified interface for linting'
                     ' and fixing the code with a single configuration file,'
                     ' regardless of the programming languages used. You can'
                     f' use {org_name} from within your favorite editor,'
                     ' integrate it with your CI and, get the results as JSON'
                     ', or customize it to your needs with its flexible'
                     ' configuration syntax.')
        context['org']['about'] = about_org
        context['quote_details'] = self.get_quote_of_the_day()
        context['top_meta_review_users'] = self.get_top_meta_review_users(
            count=5)
        context['top_gamification_users'] = self.get_top_gamification_users(
            count=5)
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
