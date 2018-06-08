import logging

from meta_review.models import Participant, Comment, Reaction


def dump_all(participants, comments, reactions):
    """
    Dump all meta-review related data into database.
    """
    dump_participants(participants)
    dump_comments(comments)
    dump_reactions(reactions)


def dump_data(cls, data):
    """
    Helper function for dumping data into database.
    """
    logger = logging.getLogger(__name__)
    logger.info('dump %s data into database' % cls.__name__.lower())
    try:
        # there's no way to do bulk update, so we delete and then create
        # bulk delete all data
        cls.objects.all().delete()
        # bulk create all data
        cls.objects.bulk_create(data.values())
    except Exception as ex:
        logger.error('Something went wrong saving %s: %s'
                     % (cls.__name__.lower(), ex))


def dump_participants(participants):
    """
    Dump participants data into Django database.
    """
    dump_data(Participant, participants)


def dump_comments(comments):
    """
    Dump comments data into Django database.
    """
    dump_data(Comment, comments)


def dump_reactions(reactions):
    """
    Dump reactions data into Django database.
    """
    dump_data(Reaction, reactions)
