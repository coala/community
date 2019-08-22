from django.db import models


class Message(models.Model):
    identifier = models.CharField(max_length=500)
    room = models.CharField(max_length=300)
    text = models.TextField()
    sent_at = models.DateTimeField()
    sent_by = models.CharField(max_length=300)
    message_type = models.CharField(max_length=100)

    def __str__(self):
        return (str(self.identifier) + ': ' + self.text)
