from django.views.generic import TemplateView

from community.views import get_header_and_footer
from data.models import Contributor


class ContributorsListView(TemplateView):
    template_name = 'contributors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        contrib_objects = Contributor.objects.all()
        context['contributors'] = contrib_objects.order_by('-num_commits',
                                                           'name')
        return context
