from meta_review.models import Participant
from django.shortcuts import render
from django.db.models import Q


def index(request):
    participants = Participant.objects.all().exclude(
        Q(pos_in=0),
        Q(neg_in=0),
        Q(pos_out=0),
        Q(neg_out=0),
        Q(offset=0)
    )
    args = {'participants': participants}
    return render(request, 'meta_review.html', args)
