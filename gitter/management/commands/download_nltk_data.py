from django.core.management.base import BaseCommand

import nltk


class Command(BaseCommand):
    help = 'Download nltk data'

    def handle(self, *args, **options):
        nltk.download('averaged_perceptron_tagger')
        nltk.download('punkt')
