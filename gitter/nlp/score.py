from gitter.nlp.tagger import MessageTagger


def value_of(sentiment):
    """
    Get a value based on the sentiment.

    :param sentiment: a string representing the sentiment of
                      a word. i.e. 'ignore' or 'question'.
    :return: an integer representing the value of the sentiment.
    """
    if sentiment == 'ignore':
        return 1
    if sentiment == 'question':
        return -1
    return 0


def sentiment_score(text):
    """
    Get the score of a message.

    :param text: a string representing the text of a message.
                 e.g. 'How to solve this issue?'
    :return: an integer representing the value of a message.
    """
    files = [
        'gitter/nlp/training_data/question.yml',
        'gitter/nlp/training_data/ignore.yml',
        ]
    message_tagger = MessageTagger(files)
    return sum(
        [value_of(tag) for sentence in message_tagger.tagged_message(
            text) for token in sentence for tag in token[2]])
