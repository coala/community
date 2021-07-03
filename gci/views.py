from django.http import HttpResponse
from datetime import datetime
from calendar import timegm
import logging
import requests

from .students import get_linked_students
from .gitorg import get_logo
from .task import get_tasks

STUDENT_URL = (
    'https://codein.withgoogle.com/dashboard/task-instances/?'
    'sp-organization={org_id}&sp-claimed_by={student_id}'
    '&sp-order=-modified&sp-my_tasks=false&sp-page_size=20'
)


def index(request):
    logger = logging.getLogger(__name__ + '.index')
    try:
        get_tasks()
    except FileNotFoundError:
        logger.info('GCI data not available')
        s = ['GCI data not available']
    else:
        s = gci_overview()

    return HttpResponse('\n'.join(s))


def gci_overview():
    logger = logging.getLogger(__name__ + '.gci_overview')
    linked_students = list(get_linked_students())
    if not linked_students:
        logger.info('No GCI students are linked')
        return ['No GCI students are linked']

    org_id = linked_students[0]['organization_id']
    org_name = linked_students[0]['organization_name']
    s = []
    s.append('<link rel="stylesheet" href="../static/main.css">')

    favicon = get_logo(org_name, 16)
    with open('_site/favicon.png', 'wb') as favicon_file:
        favicon_file.write(favicon)

    org_logo = get_logo(org_name)
    with open('_site/org_logo.png', 'wb') as org_logo_file:
        org_logo_file.write(org_logo)

    s.append('<link rel="shortcut icon" type="image/png" '
             'href="../static/favicon.png"/>')
    s.append('<img src="../static/org_logo.png" alt="'+org_name+'">')
    s.append('<h2>Welcome</h2>')
    s.append('Hello, world. You are at the {org_name} community GCI website.'
             .format(org_name=org_name))
    s.append('Students linked to %s issues:<ul class="students">' % org_name)
    for student in linked_students:
        student_id = student['id']
        username = student['username']

        r = requests.get('https://api.github.com/users/{}'.format(username))

        if r.status_code == 404:
            continue

        student_url = STUDENT_URL.format(org_id=org_id,
                                         student_id=student_id,
                                         )
        s.append('<li class="student">'
                 'STUDENT ID: <a href="{student_url}">{student_id}</a><br />'
                 '<div class="github-card" data-github="{username}" '
                 'data-width="400" data-theme="default"></div>'
                 .format(student_url=student_url, student_id=student_id,
                         username=username))

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s.append('</ul><i id="time" class="timestamp" data-time="{unix}">'
             'Last updated: {timestamp} '
             '(<span id="ago" class="timeago"></span>)</i>'
             .format(unix=timegm(datetime.utcnow().utctimetuple()),
                     timestamp=timestamp))

    s.append('<script src="//cdn.jsdelivr.net/gh/lepture/github-cards@1.0.2'
             '/jsdelivr/widget.js"></script>')
    s.append('<script src="../static/timeago.js"></script>')
    s.append('<script>loadTimeElements()</script>')

    return s
