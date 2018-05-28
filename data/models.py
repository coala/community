from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    login = models.TextField(default=None, primary_key=True)
    name = models.TextField(default=None, null=True)
    bio = models.TextField(default=None, null=True)
    num_commits = models.IntegerField(default=None, null=True)
    reviews = models.IntegerField(default=None, null=True)
    issues_opened = models.IntegerField(default=None, null=True)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['login']
