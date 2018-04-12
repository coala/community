from getorgdata.models import Participant

from django.shortcuts import render


def index(request):
    participants = Participant.objects.all()
    args = {'participants': participants}
    return render(request, 'getorgdata.html', args)
