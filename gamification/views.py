from django.views.generic import TemplateView

from community.views import get_header_and_footer
from gamification.models import Participant


class GamificationResults(TemplateView):
    template_name = 'gamification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['gamification_results'] = Participant.objects.all()
        return context
