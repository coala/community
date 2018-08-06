from data.newcomers import active_newcomers
from gamification.models import Participant


def create_participants():
    """
    Create participants which will be used in the gamification system.
    """
    participant_objects_list = []
    for participant in active_newcomers():
        participant_objects_list.append(
            Participant(username=participant))
    Participant.objects.bulk_create(participant_objects_list)
