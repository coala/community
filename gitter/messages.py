import logging

import requests

from data.webservices import webservices_url
from gitter.nlp.score import sentiment_score
from gitter.models import Message


def get_messages():
    """
    Get all the messages send by newcomers on the gitter rooms.
    """
    logger = logging.getLogger(__name__)
    import_url = webservices_url('messages')
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(
            url=import_url,
            headers=headers,
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
        return

    data = response.json()
    return data


def message_type(message):
    """
    Get the type of a message from a message_dict.

    :param message: a message dict of type:
                    {
                       "identifier": "5b588269c0fa8016e7379191",
                       "room": "offtopic",
                       "sent_at": "2018-07-25 14:00:09.456000+00:00",
                       "sent_by": "Naveenaidu",
                       "text": "How can I solve this issue?",
                    },
    :return: a string representing the type of the message.
             i.e. 'question' or 'answer'.

    """
    text = message['text']
    score = sentiment_score(text)
    if score >= 0:
        if len(text) > 60:
            m_type = 'answer'
        else:
            m_type = 'ignore'
        return m_type
    else:
        m_type = 'question'
        return m_type


def import_messages(messages):
    message_objects_list = []
    for message in messages:
        m_type = message_type(message)
        message['message_type'] = m_type
        message_objects_list.append(Message(**message))
    Message.objects.bulk_create(message_objects_list)
