from django.views import generic

from community.views import get_header_and_footer
from openhub_django.models import (
    PortfolioProject,
    OutsideProject,
    OutsideCommitter,
    AffiliatedCommitter,
    Organization,
    )


class Homepage(generic.TemplateView):
    template_name = 'openhub_django/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['portfolioprojects'] = 'portfolio_projects'
        context['outsidecommitters'] = 'outside_committers'
        context['affiliatedcommitters'] = 'affiliated_committers'
        context['outsideprojects'] = 'outside_projects'
        context['organization'] = 'organization'
        return context


class PortfolioProjectListView(generic.ListView):
    model = PortfolioProject
    context_object_name = 'portfolio_project_list'
    template_name = 'openhub_django/portfolioproject_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class PortfolioProjectDetailView(generic.DetailView):
    model = PortfolioProject
    template_name = 'openhub_django/portfolioproject_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OutsideProjectListView(generic.ListView):
    model = OutsideProject
    context_object_name = 'outside_project_list'
    template_name = 'openhub_django/outsideproject_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OutsideProjectDetailView(generic.DetailView):
    model = OutsideProject
    template_name = 'openhub_django/outsideproject_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OutsideCommitterListView(generic.ListView):
    model = OutsideCommitter
    context_object_name = 'outside_committer_list'
    template_name = 'openhub_django/outsidecommitter_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OutsideCommitterDetailView(generic.DetailView):
    model = OutsideCommitter
    template_name = 'openhub_django/outsidecommitter_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class AffiliatedCommitterListView(generic.ListView):
    model = AffiliatedCommitter
    context_object_name = 'affiliated_committer_list'
    template_name = 'openhub_django/affiliatedcommitter_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class AffiliatedCommitterDetailView(generic.DetailView):
    model = AffiliatedCommitter
    template_name = 'openhub_django/affiliatedcommitter_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OrganizationListView(generic.ListView):
    model = Organization
    context_object_name = 'organization_list'
    template_name = 'openhub_django/organization_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context


class OrganizationDetailView(generic.DetailView):
    model = Organization
    template_name = 'openhub_django/organization_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        return context
