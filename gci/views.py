from datetime import datetime
from calendar import timegm

import logging

from django.views.generic import TemplateView

from community.views import get_header_and_footer
from data.models import Contributor
from .students import get_linked_students
from .task import get_tasks

STUDENT_URL = (
    'https://codein.withgoogle.com/dashboard/task-instances/?'
    'sp-organization={org_id}&sp-claimed_by={student_id}'
    '&sp-order=-modified&sp-my_tasks=false&sp-page_size=20'
)


class GCIStudentsList(TemplateView):
    template_name = 'gci_students.html'

    def get_data_updated_time(self):
        return timegm(datetime.utcnow().utctimetuple())

    def get_all_students(self):
        """
        Get all GCI students by filtering the tasks that are valid
        :return: A List of all students dict having necessary information
        about the student
        """
        logger = logging.getLogger(__name__ + '.gci_overview')
        linked_students = list(get_linked_students())
        data = {
            'students': list(),
            'error': None
        }
        if not linked_students:
            error_message = 'No GCI students are linked'
            logger.info(error_message)
            data['error'] = error_message
            return data
        org_id = linked_students[0]['organization_id']
        for student in linked_students:
            student_id = student['id']
            username = student['username']
            contributors = Contributor.objects.filter(login=username)
            if contributors:
                contrib = contributors.first()
                student['url'] = STUDENT_URL.format(org_id=org_id,
                                                    student_id=student_id)
                student['name'] = contrib.name
                student['bio'] = contrib.bio
                student['public_repos'] = contrib.public_repos
                student['public_gists'] = contrib.public_gists
                student['followers'] = contrib.followers
                data['students'].append(student)
            else:
                logger.warning(f"GCI Student {username} doesn't exists!"
                               f' Please check the username.')
        return data

    def get_gci_tasks_and_students(self):
        """
        Get all GCI students by fetching the GCI tasks and the students
        :return: A list of all GCI Students
        """
        logger = logging.getLogger(__name__ + '.index')
        gci_students = {
            'data': {},
            'error': None
        }
        try:
            get_tasks()
        except FileNotFoundError:
            logger.info('GCI data not available')
            error_message = ('No GCI data is available. Please create a'
                             ' tasks.yaml file having GCI tasks related'
                             ' data in it.')
            gci_students['error'] = error_message
        else:
            data = self.get_all_students()
            if data['error']:
                gci_students['error'] = data['error']
            else:
                gci_students['data'] = data['students']
        return gci_students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['gci_students'] = self.get_gci_tasks_and_students()
        context['updated_time'] = self.get_data_updated_time()
        return context
