from django.test import TestCase

from gitter.messages import message_type


class MessageAssertion(TestCase):

    def assertIsQuestion(self, message):
        message_dict = {}
        message_dict['text'] = message
        type_of_message = message_type(message_dict)
        if type_of_message != 'question':
            raise AssertionError('This message is not a question')

    def assertIsAnswer(self, message):
        message_dict = {}
        message_dict['text'] = message
        type_of_message = message_type(message_dict)
        if type_of_message != 'answer':
            raise AssertionError('This message is not a answer')

    def assertIsIgnore(self, message):
        message_dict = {}
        message_dict['text'] = message
        type_of_message = message_type(message_dict)
        if type_of_message != 'ignore':
            raise AssertionError('This message is not a ignore')
