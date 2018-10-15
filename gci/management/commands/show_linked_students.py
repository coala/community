from django.core.management.base import BaseCommand

from gci.students import get_linked_students


class Command(BaseCommand):
    help = 'Show linked students'

    def handle(self, *args, **options):
        linked_students = list(get_linked_students())
        for student in linked_students:
            student_id = student['id']
            username = student['username']
            print(f'{student_id} = {username}')
