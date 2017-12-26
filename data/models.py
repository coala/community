from django.db import models
import json
# Create your models here.


class Repo(models.Model):
    name = models.TextField(default=None, primary_key=True)
    repo_data = models.TextField(default=None, null=True)
    contributors_data = models.TextField(default=None, null=True)

    def repo_data_to_json(self, repo_data):
        self.repo_data = json.dumps(repo_data)

    def repo_data_from_json(self):
        return json.loads(self.repo_data)

    def contributors_data_to_json(self, repo_data):
        self.contributors_data = json.dumps(repo_data)

    def contributors_data_from_json(self):
        return json.loads(self.contributors_data)


class Contributor(models.Model):
    login = models.TextField(default=None, primary_key=True)
    name = models.TextField(default=None, null=True)
    bio = models.TextField(default=None, null=True)
    num_commits = models.IntegerField(default=None, null=True)
    reviews = models.IntegerField(default=None, null=True)
    issues_opened = models.IntegerField(default=None, null=True)
