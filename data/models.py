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
    image_url = models.ImageField(default=None, null=True)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['login']


class Label(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Issue(models.Model):
    number = models.IntegerField()
    title = models.TextField()
    repo = models.CharField(max_length=100, default=None, null=True)
    repo_id = models.IntegerField()
    author = models.ForeignKey(Contributor,
                               on_delete=models.CASCADE,
                               related_name='issue_author')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    state = models.CharField(max_length=100)
    labels = models.ManyToManyField(Label, blank=True)
    assignees = models.ManyToManyField(Contributor,
                                       related_name='issue_assignees',
                                       blank=True)
    hoster = models.CharField(max_length=100)
    url = models.URLField(null=True)

    def __str__(self):
        return str(self.title)


class IssueNumber(models.Model):
    number = models.IntegerField()
    repo_id = models.IntegerField()

    def __str__(self):
        return str(self.number)

    def get_issue(self):
        """
        Get an issue object which number mathes with the
        issue number and has same repo_id.
        """
        issue = Issue.objects.get(number=self.number,
                                  repo_id=self.repo_id)
        return issue


class MergeRequest(models.Model):
    number = models.IntegerField()
    title = models.TextField()
    repo_id = models.IntegerField()
    repo = models.CharField(max_length=100, default=None, null=True)
    closes_issues = models.ManyToManyField(IssueNumber, blank=True)
    state = models.CharField(max_length=100)
    author = models.ForeignKey(Contributor,
                               on_delete=models.CASCADE,
                               related_name='mr_author')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    assignees = models.ManyToManyField(Contributor,
                                       related_name='mr_assignees',
                                       blank=True)
    ci_status = models.BooleanField()
    labels = models.ManyToManyField(Label, blank=True)
    hoster = models.CharField(max_length=100)
    url = models.URLField(null=True)

    def __str__(self):
        return self.title

    def get_closes_issues_object(self):
        """
        Get the list of issues object this mr is closing.
        """
        issues_object_list = []
        issue_numbers = self.closes_issues.all()
        for issue_number in issue_numbers:
            issue_object = issue_number.get_issue()
            issues_object_list.append(issue_object)
        return issues_object_list
