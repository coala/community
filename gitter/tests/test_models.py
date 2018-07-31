from django.test import TestCase

from gitter.models import Message


class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Message.objects.create(identifier='5b5f1dc4d4527523f640004c',
                               room='test/test',
                               text='Is this issue valid?',
                               sent_at='2018-07-25 14:00:09.456000',
                               sent_by='testuser',
                               message_type='question')

    def test_field_label(self):
        message = Message.objects.get(identifier='5b5f1dc4d4527523f640004c')
        identifier = message._meta.get_field('identifier').verbose_name
        room = message._meta.get_field('room').verbose_name
        text = message._meta.get_field('text').verbose_name
        sent_at = message._meta.get_field('sent_at').verbose_name
        sent_by = message._meta.get_field('sent_by').verbose_name
        message_type = message._meta.get_field('message_type').verbose_name
        self.assertEquals(identifier, 'identifier')
        self.assertEquals(room, 'room')
        self.assertEquals(text, 'text')
        self.assertEquals(sent_at, 'sent at')
        self.assertEquals(sent_by, 'sent by')
        self.assertEquals(message_type, 'message type')

    def test_object_name_is_repr_return(self):
        message = Message.objects.get(identifier='5b5f1dc4d4527523f640004c')
        expected_object_name = '5b5f1dc4d4527523f640004c: Is this issue valid?'
        self.assertEquals(expected_object_name, str(message))
