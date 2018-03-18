from django.shortcuts import render

from openhub.models import PortfolioProject


def index(request):
    projects = PortfolioProject.objects.all()
    args = {'projects': projects}
    return render(request, 'openhub.html', args)
