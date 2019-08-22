from gitter.nlp.splitter import Splitter
from gitter.nlp.pos_tagger import POSTagger
from gitter.nlp.dict_tagger import DictionaryTagger


class MessageTagger:

    def __init__(self, files):
        self.splitter = Splitter()
        self.postagger = POSTagger()
        self.dicttagger = DictionaryTagger(files)

    def tagged_message(self, text):
        """
        Process a message with NLP classes.

        Step-1: Use Splitter class to split the text message
                into list of lists of word.

        Step-2: Use POSTagger class to tag the splitted message
                with pos.

        Step-3: Use DictionaryTagger to tag the message based on
                provided dictionaries. i.e. 'training_data/question.yml'
                and 'training_data/answers.yml'.

        :param text: a string representing the message.
                     e.g. 'How to solve this issue?'
        :return: a list of lists of words tagged with DictionaryTagger
                 and POSTagger.
                 e.g. [[('how', 'how', ['question', 'WRB']),
                        ('can', 'can', ['MD']),
                        ('I', 'I', ['PRP']),
                        ('solve', 'solve', ['VB']),
                        ('this', 'this', ['DT']),
                        ('issue', 'issue', ['NN']),
                        ('?', '?', ['question', '.'])]]
        """
        splitted_message = self.splitter.split(text)
        pos_tagged_message = self.postagger.pos_tag(splitted_message)
        dict_tagged_message = self.dicttagger.tag(pos_tagged_message)
        return dict_tagged_message
