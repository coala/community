from meta_review.models import Participant
from django.db.models import Q
from django.views.generic import TemplateView

from community.views import get_header_and_footer


class ContributorsMetaReview(TemplateView):
    template_name = 'meta_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        participants = Participant.objects.all().exclude(
            Q(pos_in=0),
            Q(neg_in=0),
            Q(pos_out=0),
            Q(neg_out=0),
            Q(offset=0)
        )
        context['contributors_meta_review_details'] = participants
        return context
