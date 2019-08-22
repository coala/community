import nltk


class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        Split a paragraph into list of lists of words.

        :param text: a paragraph of text
        :return: a list of lists of words.
                 e.g.: [['this', 'is', 'a', 'sentence'],
                 ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [
            self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences
