from django.db import models
from django.urls import reverse


class OpenhubOrganization(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField(null=True)
    html_url = models.URLField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    homepage_url = models.URLField(null=True)
    vanity_url = models.CharField(null=True, max_length=200, blank=True)
    org_type = models.CharField(max_length=100)
    medium_logo_url = models.URLField(null=True)
    small_logo_url = models.URLField(null=True)
    projects_count = models.IntegerField(default=0)
    affiliated_committers = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:

        ordering = ['name']


class PortfolioProjectActivity(models.Model):

    commits = models.IntegerField(null=True)
    change_in_commits = models.IntegerField(null=True)
    percentage_change_in_commits = models.IntegerField(null=True)
    contributors = models.IntegerField(null=True)
    change_in_contributors = models.IntegerField(null=True)
    percentage_change_in_committers = models.IntegerField(null=True)

    def __str__(self):
        return str(self.commits)


class PortfolioProject(models.Model):

    name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    i_use_this = models.IntegerField()
    community_rating = models.FloatField(null=True)
    primary_language = models.CharField(max_length=100)
    org = models.CharField(max_length=200)
    twelve_mo_activity_and_year_on_year_change = (
        models.ForeignKey(PortfolioProjectActivity,
                          on_delete=models.CASCADE))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular portfolio project instance.
        """
        return reverse('portfolioproject-detail', args=[str(self.id)])


class OutsideProject(models.Model):

    name = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    claimed_by = models.CharField(max_length=100, null=True)
    i_use_this = models.IntegerField(null=True)
    community_rating = models.FloatField(null=True)
    affiliates_contributing = models.IntegerField(null=True)
    commits_by_current_affiliates = models.IntegerField(null=True)
    org = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('outsideproject-detail', args=[str(self.id)])


class ContributionsToPortfolioProject(models.Model):

    projects = models.TextField()
    twelve_mo_commits = models.IntegerField()

    def __str__(self):
        return self.projects


class OutsideCommitter(models.Model):

    name = models.CharField(max_length=100)
    kudos = models.IntegerField(null=True)
    level = models.IntegerField()
    affiliated_with = models.CharField(max_length=100)
    org = models.CharField(max_length=100)
    contributions_to_portfolio_projects = (
        models.ForeignKey(ContributionsToPortfolioProject,
                          on_delete=models.CASCADE))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('outsidecommitter-detail', args=[str(self.id)])


class MostCommit(models.Model):

    project = models.CharField(max_length=100)
    commits = models.IntegerField()

    def __str__(self):
        return self.project


class MostRecentCommit(models.Model):

    project = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    def __str__(self):
        return self.project


class AffiliatedCommitter(models.Model):

    org = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    kudos = models.IntegerField(null=True)
    level = models.IntegerField()
    most_commits = (
        models.ForeignKey(MostCommit, on_delete=models.CASCADE))
    most_recent_commit = (
        models.ForeignKey(MostRecentCommit, on_delete=models.CASCADE))

    def __str__(self):
        return self.org

    def get_absolute_url(self):
        return reverse('affiliatedcommitter-detail', args=[str(self.id)])


class InfographicDetail(models.Model):

    outside_committers = models.IntegerField(null=True)
    outside_committers_commits = models.IntegerField(null=True)
    projects_having_outside_commits = models.IntegerField(null=True)
    portfolio_projects = models.IntegerField(null=True)
    affiliators = models.IntegerField(null=True)
    affiliators_committing_to_portfolio_projects = (
        models.IntegerField(null=True))
    affiliator_commits_to_portfolio_projects = (
        models.IntegerField(null=True))
    affiliators_commiting_projects = models.IntegerField(null=True)
    outside_projects = models.IntegerField(null=True)
    outside_projects_commits = models.IntegerField(null=True)
    affiliators_committing_to_outside_projects = (
        models.IntegerField(null=True))

    def __str__(self):
        return str(self.outside_committers)


class Organization(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField(null=True)
    html_url = models.URLField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    homepage_url = models.URLField(null=True)
    url_name = models.CharField(max_length=100, null=True, blank=True)
    org_type = models.CharField(max_length=100, null=True)
    medium_logo_url = models.URLField(null=True)
    small_logo_url = models.URLField(null=True)
    infographic_details = (
        models.OneToOneField(InfographicDetail,
                             on_delete=models.CASCADE, null=True))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org-detail', args=[str(self.id)])
