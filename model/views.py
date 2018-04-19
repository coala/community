from django.shortcuts import render
from django.views import generic

from openhub.models import (
    PortfolioProject,
    OutsideProject,
    OutsideCommitter,
    AffiliatedCommitter,
    Organization,
    )


def index(request):
    args = {
        'portfolioprojects': 'portfolio_projects',
        'outsidecommitters': 'outside_committers',
        'affiliatedcommitters': 'affiliated_committers',
        'outsideprojects': 'outside_projects',
        'organization': 'organization',
        }
    return render(request, 'model.html', args)


class PortfolioProjectListView(generic.ListView):
    model = PortfolioProject
    context_object_name = 'portfolio_project_list'
    template_name = 'model/templates/portfolio_project_list.html'


class PortfolioProjectDetailView(generic.DetailView):
    model = PortfolioProject
    template_name = 'model/templates/portfolio_project_detail.html'


class OutsideProjectListView(generic.ListView):
    model = OutsideProject
    context_object_name = 'outside_project_list'
    template_name = 'model/templates/outside_project_list.html'


class OutsideProjectDetailView(generic.DetailView):
    model = OutsideProject
    template_name = 'model/templates/outside_project_detail.html'


class OutsideCommitterListView(generic.ListView):
    model = OutsideCommitter
    context_object_name = 'outside_committer_list'
    template_name = 'model/templates/outside_committer_list.html'


class OutsideCommitterDetailView(generic.DetailView):
    model = OutsideCommitter
    template_name = 'model/templates/outside_committer_detail.html'


class AffiliatedCommitterListView(generic.ListView):
    model = AffiliatedCommitter
    context_object_name = 'affiliated_committer_list'
    template_name = 'model/templates/affiliated_committer_list.html'


class AffiliatedCommitterDetailView(generic.DetailView):
    model = AffiliatedCommitter
    template_name = 'model/templates/affiliated_committer_detail.html'


class OrganizationListView(generic.ListView):
    model = Organization
    context_object_name = 'organization_list'
    template_name = 'model/templates/organization_list.html'


class OrganizationDetailView(generic.DetailView):
    model = Organization
    template_name = 'model/templates/organization_detail.html'
