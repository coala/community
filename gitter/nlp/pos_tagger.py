import nltk


class POSTagger(object):

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'],
            ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens.
        Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']),
                 ('is', 'be', ['VB']), ('a', 'a', ['DT']),
                 ('sentence', 'sentence', ['NN'])],
                 [('this', 'this', ['DT']), ('is', 'be', ['VB']),
                 ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence]
               for sentence in pos]
        return pos
