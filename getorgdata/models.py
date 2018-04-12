from django.db import models
from geoposition.fields import GeopositionField


class Getorg(models.Model):
    org_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    position = GeopositionField(blank=True)
    org_name = models.OneToOneField(Getorg, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(models.Model):
    identifier = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Label(models.Model):
    identifier = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class PullRequest(models.Model):
    identifier = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    html_url = models.URLField()
    target_repository = models.CharField(max_length=100)
    source_repository = models.CharField(max_length=100)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    tests_passed = models.BooleanField()
    author = models.ManyToManyField(User)
    title = models.TextField()
    description = models.TextField()
    state = models.CharField(max_length=100)
    comments = models.IntegerField()

    def __str__(self):
        return self.title


class Issue(models.Model):
    identifier = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    author = models.CharField(max_length=100)
    assignees = models.ManyToManyField(User)
    labels = models.ManyToManyField(Label)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    repository = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    comments = models.IntegerField()
    org = models.OneToOneField(Getorg, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
