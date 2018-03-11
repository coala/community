from data.models import Contributor
from django.shortcuts import render


def index(request):
    contributors = Contributor.objects.all()
    args = {'contributors': contributors}
    return render(request, 'contributors.html', args)
