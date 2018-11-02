from django.shortcuts import render

from openhub.models import PortfolioProject
from openhub.oh_token import OH_TOKEN


def index(request):
    errors = []
    projects = []
    if OH_TOKEN is None:
        errors.append("""
        OH_TOKEN is not specified as an environment variable. <br/>
        You can get an OpenHub token by signing up at
        <a href="https://www.openhub.net">openhub.net</a>.
        """)
    else:
        projects = PortfolioProject.objects.all()

    args = {'projects': projects, 'errors': errors}
    return render(request, 'openhub.html', args)
