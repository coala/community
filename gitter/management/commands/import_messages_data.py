from django.core.management.base import BaseCommand

from gitter.messages import get_messages, import_messages


class Command(BaseCommand):
    help = 'Import Newcomer Messages'

    def handle(self, *args, **options):
        messages = get_messages()
        if messages:
            import_messages(messages)
