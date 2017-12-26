import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_common.http import HttpResponse
from org.models import Contributor

from brake.decorators import ratelimit


@ratelimit(block=True, rate='50/m')
@csrf_exempt
@require_http_methods(['GET'])
def contrib(request):
    response = Contributor.objects.all()
    data = [{'name': item.name,
             'issues': item.issues_opened,
             'contributions': item.num_commits,
             'bio': item.bio,
             'login': item.login,
             'reviews': item.reviews
             } for item in response]
    return HttpResponse(json.dumps(data), content_type='application/json')
