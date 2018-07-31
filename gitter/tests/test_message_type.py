from gitter.tests.message_assertions import MessageAssertion


class MessgeTypeTest(MessageAssertion):

    def test_ignore_message(self):
        """
        This method is responsible for testing the positive
        sentiment score. It means that the message should be ignored.
        """
        self.assertIsIgnore('Please assign me this issue')
        self.assertIsIgnore('Thank you.')
        self.assertIsIgnore('Okay thank you so much :)')
        self.assertIsIgnore('I have replied to your comment')
        self.assertIsIgnore('OK thanks i got it')
        self.assertIsIgnore('ok Cool')
        self.assertIsIgnore('I have made the PR')
        self.assertIsIgnore('Yes, pushing the commit.')
        self.assertIsIgnore('Thanks a lot! Its working now :D')
        self.assertIsIgnore('I\'ll check them again.')
        self.assertIsIgnore('I tried it locally and it works')
        self.assertIsIgnore('I\'ll try never to repeat these mistakes again.')
        self.assertIsIgnore('It still doesnt open up the pr')
        self.assertIsIgnore('Cool ill do that')
        self.assertIsIgnore('Okay .....then I will wait.Anyways thank you')
        self.assertIsIgnore('Ok thank you, sorry for the multipost')
        self.assertIsIgnore('Okay thanks! And I saw it, will fix it quick.')
        self.assertIsIgnore('Thanks. I read first I have to run on a project.')
        self.assertIsIgnore(
            'Please @jayvdb can help me with solving this issue.')

    def test_question_message(self):
        """
        This method is responsible for testing the positive
        sentiment score. It means that the message should be ignored.
        """
        self.assertIsQuestion('I\'ve got a question can i use the corobo '
                              'commands in any channel or is there a '
                              'special channel?')
        self.assertIsQuestion('Can someone tell me if this pr is okay '
                              'or it needs more changes? ')
        self.assertIsQuestion('Can I work on this?')
        self.assertIsQuestion('Can someone assign to me?')
        self.assertIsQuestion('How did you put a tickmark on a commit ?')
        self.assertIsQuestion('what to do after rebase?')
        self.assertIsQuestion('how to Use github interface for review?')
        self.assertIsQuestion('But dont i have to wait for my previous '
                              'PR to get merged?')
        self.assertIsQuestion('is there a separate bears room?')
        self.assertIsQuestion('What does invoking with a single option mean?')
        self.assertIsQuestion('Any hint in which file should i add this test?')
        self.assertIsQuestion('Should i click on the create pull request?')
        self.assertIsQuestion('is the bot down?')
        self.assertIsQuestion('can someone tell me which is the docstring '
                              'file in -utils')
        self.assertIsQuestion('I have done a newcomer issue, and also '
                              'reviewed a newcomer issue, What furthere '
                              'steps for becoming a developer?')
        self.assertIsQuestion(
            'ok, can you give me some more time to work on this?')
        self.assertIsQuestion('I had a question why is corobo down?')
        self.assertIsQuestion('ok, so what should I do now?')
        self.assertIsQuestion('Okay I will stick to it but why will '
                              'he won\'t approve it?')
        self.assertIsQuestion('How do you squash a commit? I\'m '
                              'sorry I\'m new to this.')
        self.assertIsQuestion(
            'I actually used that guide, did I do something wrong?')
        self.assertIsQuestion('Do i need to wait for it to be merged?')
        self.assertIsQuestion('Hi, may i know why the bot check for '
                              'failed for continuous-integration?')
        self.assertIsQuestion('Should i add the file , commit and push?')
        self.assertIsQuestion('so how to go about it?')
        self.assertIsQuestion('does bear support python 3.7?')

    def test_answer_message(self):
        """
        This method is responsible for testing the positive
        sentiment score. It means that the message should be ignored.
        """
        self.assertIsAnswer('The commit looks good to me .You can '
                            'wait for it to get merged.')
        self.assertIsAnswer('No create a pull request.The Travis CI '
                            'build will continue its checking.')
