import os

import logging

import requests

from trav import Travis

from django.views.generic.base import TemplateView
from django.views.generic import ListView

from .git import (
    get_org_name,
    get_remote_url
)
from .forms import (
    JoinCommunityForm,
    CommunityGoogleForm,
    CommunityEvent,
    OrganizationMentor,
    GSOCStudent,
    AssignIssue,
    NewcomerPromotion,
    Feedback
)
from data.models import Team, InactiveIssue
from gamification.models import Participant as GamificationParticipant
from meta_review.models import Participant as MetaReviewer

GL_NEWCOMERS_GRP = 'https://gitlab.com/{}/roles/newcomers'.format(
    get_org_name()
)


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


def get_feedback_form_variables(context):
    context['feedback_form'] = Feedback()
    context['feedback_form_name'] = os.environ.get(
        'FEEDBACK_FORM_NAME', None
    )
    return context


def get_newcomer_promotion_form_variables(context):
    context['newcomer_promotion_form'] = NewcomerPromotion()
    context['newcomer_promotion_form_name'] = os.environ.get(
        'NEWCOMER_PROMOTION_REQUEST_FORM_NAME', None
    )
    return context


def get_assign_issue_form_variables(context):
    context['assign_issue_form'] = AssignIssue()
    context['assign_issue_form_name'] = os.environ.get(
        'ISSUES_ASSIGN_REQUEST_FORM_NAME', None
    )
    return context


def get_gsoc_student_form_variables(context):
    context['gsoc_student_form'] = GSOCStudent()
    context['gsoc_student_form_name'] = os.environ.get(
        'GSOC_STUDENT_FORM_NAME', None
    )
    return context


def get_community_mentor_form_variables(context):
    context['organization_mentor_form'] = OrganizationMentor()
    context['organization_mentor_form_name'] = os.environ.get(
        'MENTOR_FORM_NAME', None
    )
    return context


def get_community_event_form_variables(context):
    context['community_event_form'] = CommunityEvent()
    context['community_event_form_name'] = os.environ.get(
        'CALENDAR_NETLIFY_FORM_NAME', None
    )
    return context


def get_community_google_form_variables(context):
    context['community_google_form'] = CommunityGoogleForm()
    context['community_google_form_name'] = os.environ.get(
        'OSFORMS_NETLIFY_FORM_NAME', None
    )
    return context


def get_all_community_forms(context):
    context = get_community_google_form_variables(context)
    context = get_community_event_form_variables(context)
    context = get_community_mentor_form_variables(context)
    context = get_gsoc_student_form_variables(context)
    context = get_assign_issue_form_variables(context)
    context = get_newcomer_promotion_form_variables(context)
    context = get_feedback_form_variables(context)
    return context


def get_header_and_footer(context):
    context['isTravis'] = Travis.TRAVIS
    context['travisLink'] = Travis.TRAVIS_BUILD_WEB_URL
    context['org'] = initialize_org_context_details()
    context = get_all_community_forms(context)
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


class JoinCommunityView(TemplateView):

    template_name = 'join_community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['join_community_form'] = JoinCommunityForm()
        context['gitlab_newcomers_group_url'] = GL_NEWCOMERS_GRP
        context['join_community_form_name'] = os.environ.get(
            'JOIN_COMMUNITY_FORM_NAME', None
        )
        return context


class OrganizationTeams(ListView):

    template_name = 'teams.html'
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class InactiveIssuesList(ListView):

    template_name = 'issues.html'
    model = InactiveIssue
    ordering = 'hoster'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['page_name'] = 'Inactive Issues List'
        return context
