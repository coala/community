from dateutil.parser import parse
import pytz

from django.test import TestCase

from data.models import (
    Contributor,
    Label,
    IssueNumber,
    Issue,
    MergeRequest,
    )
from community.git import get_org_name


class ContributorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Contributor.objects.create(login='test', name='Test User')
        Contributor.objects.create(login='sks444', name='Shrikrishna Singh')

    def test_field_label(self):
        contributor = Contributor.objects.get(login='sks444')
        login = contributor._meta.get_field('login').verbose_name
        name = contributor._meta.get_field('name').verbose_name
        bio = contributor._meta.get_field('bio').verbose_name
        num_commits = (
            contributor._meta.get_field('num_commits').verbose_name)
        reviews = contributor._meta.get_field('reviews').verbose_name
        issues_opened = contributor._meta.get_field(
            'issues_opened').verbose_name
        self.assertEquals(login, 'login')
        self.assertEquals(name, 'name')
        self.assertEquals(bio, 'bio')
        self.assertEquals(num_commits, 'num commits')
        self.assertEquals(reviews, 'reviews')
        self.assertEquals(issues_opened, 'issues opened')

    def test_object_name_is_login(self):
        contributor = Contributor.objects.get(login='sks444')
        expected_object_name = 'sks444'
        self.assertEquals(expected_object_name, str(contributor))

    def test_class_meta_ordering(self):
        contributors = Contributor.objects.all()
        self.assertEquals(contributors[0].login, 'sks444')
        self.assertEquals(contributors[1].login, 'test')


class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        Label.objects.create(name='difficulty/newcomer')

    def test_field_label(self):
        label = Label.objects.get(id=1)
        name = label._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

    def test_object_name_is_name(self):
        label = Label.objects.get(id=1)
        expected_object_name = 'difficulty/newcomer'
        self.assertEquals(expected_object_name, str(label))


class IssueModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        contributor = Contributor.objects.create(login='sks444',
                                                 name='Shrikrishna Singh')
        label = Label.objects.create(name='difficulty/newcomer')
        created_at = pytz.utc.localize(parse('2017-11-07T08:01:21'))
        updated_at = pytz.utc.localize(parse('2018-03-18T00:00:11'))
        issue = Issue.objects.create(number=1,
                                     title='Test issue',
                                     repo_id=1,
                                     author=contributor,
                                     created_at=created_at,
                                     updated_at=updated_at,
                                     state='open',
                                     hoster='GitHub')
        issue.labels.add(label)
        issue.assignees.add(contributor)

    def test_field_label(self):
        issue = Issue.objects.get(number=1)
        number = issue._meta.get_field('number').verbose_name
        title = issue._meta.get_field('title').verbose_name
        repo_id = issue._meta.get_field('repo_id').verbose_name
        repo = issue._meta.get_field('repo').verbose_name
        author = issue._meta.get_field('author').verbose_name
        created_at = issue._meta.get_field(
            'created_at').verbose_name
        updated_at = issue._meta.get_field(
            'updated_at').verbose_name
        state = issue._meta.get_field('state').verbose_name
        hoster = issue._meta.get_field('hoster').verbose_name
        labels = issue._meta.get_field('labels').verbose_name
        assignees = issue._meta.get_field(
            'assignees').verbose_name
        url = issue._meta.get_field('url').verbose_name
        self.assertEquals(number, 'number')
        self.assertEquals(title, 'title')
        self.assertEquals(repo_id, 'repo id')
        self.assertEquals(repo, 'repo')
        self.assertEquals(author, 'author')
        self.assertEquals(created_at, 'created at')
        self.assertEquals(updated_at, 'updated at')
        self.assertEquals(state, 'state')
        self.assertEquals(hoster, 'hoster')
        self.assertEquals(labels, 'labels')
        self.assertEquals(assignees, 'assignees')
        self.assertEquals(url, 'url')

    def test_object_name_is_title(self):
        issue = Issue.objects.get(number=1)
        expected_object_name = 'Test issue'
        self.assertEquals(expected_object_name, str(issue))

    def test_many_to_many_field(self):
        issue = Issue.objects.get(number=1)
        label = Label.objects.get(id=1)
        assignee = Contributor.objects.get(login='sks444')

        # Test issue has many to many field with label
        self.assertEquals(issue.labels.get(pk=label.pk),
                          label)

        # Test issue has many to many field with contributor
        self.assertEquals(issue.assignees.get(pk=assignee.pk),
                          assignee)


class IssueNumberModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        contributor = Contributor.objects.create(login='Abhisek-')
        created_at = pytz.utc.localize(parse('2016-12-13 17:45:38'))
        updated_at = pytz.utc.localize(parse('2017-12-21 00:01:23'))
        org_name = get_org_name()
        repo = org_name + '/' + org_name + '-quickstart'
        Issue.objects.create(number=57,
                             repo=repo,
                             title='Remove the python 3.3.6 dependency',
                             repo_id=52889504,
                             author=contributor,
                             created_at=created_at,
                             updated_at=updated_at,
                             state='closed',
                             hoster='GitHub')
        IssueNumber.objects.create(number=57, repo_id=52889504)

    def test_field_label(self):
        issue_number = IssueNumber.objects.get(number=57)
        number = issue_number._meta.get_field('number').verbose_name
        repo_id = issue_number._meta.get_field('repo_id').verbose_name
        self.assertEquals(number, 'number')
        self.assertEquals(repo_id, 'repo id')

    def test_object_name_is_number(self):
        issue_number = IssueNumber.objects.get(number=57)
        expected_object_name = '57'
        self.assertEquals(expected_object_name, str(issue_number))

    def test_get_issue(self):
        issue_number = IssueNumber.objects.get(number=57,
                                               repo_id=52889504)
        issue = Issue.objects.get(number=57, repo_id=52889504)

        # Get the issue object from the method
        issue_object = issue_number.get_issue()

        # Both object should be equal
        self.assertEquals(issue, issue_object)


class MergeRequestModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all methods
        contributor = Contributor.objects.create(login='sks444',
                                                 name='Shrikrishna Singh')
        label = Label.objects.create(name='status/STALE')
        created_at = pytz.utc.localize(parse('2016-12-13 18:11:57'))
        updated_at = pytz.utc.localize(parse('2016-12-20 06:48:23'))
        org_name = get_org_name()
        repo = org_name + '/' + org_name + '-quickstart'
        mr = MergeRequest.objects.create(number=58,
                                         repo=repo,
                                         title='Removed python 3.3 dependency',
                                         repo_id=52889504,
                                         author=contributor,
                                         created_at=created_at,
                                         updated_at=updated_at,
                                         state='merged',
                                         hoster='GitHub',
                                         ci_status=1)
        issue = IssueNumber.objects.create(number=57, repo_id=52889504)
        mr.closes_issues.add(issue)
        mr.labels.add(label)
        mr.assignees.add(contributor)
        Issue.objects.create(number=57,
                             repo=repo,
                             title='Remove the python 3.3.6 dependency',
                             repo_id=52889504,
                             author=contributor,
                             created_at=created_at,
                             updated_at=updated_at,
                             state='closed',
                             hoster='GitHub')

    def test_field_label(self):
        mr = MergeRequest.objects.get(number=58, repo_id=52889504)
        number = mr._meta.get_field('number').verbose_name
        title = mr._meta.get_field('title').verbose_name
        repo_id = mr._meta.get_field('repo_id').verbose_name
        repo = mr._meta.get_field('repo').verbose_name
        author = mr._meta.get_field('author').verbose_name
        created_at = mr._meta.get_field(
            'created_at').verbose_name
        updated_at = mr._meta.get_field(
            'updated_at').verbose_name
        state = mr._meta.get_field('state').verbose_name
        hoster = mr._meta.get_field('hoster').verbose_name
        ci_status = mr._meta.get_field('ci_status').verbose_name
        labels = mr._meta.get_field('labels').verbose_name
        assignees = mr._meta.get_field(
            'assignees').verbose_name
        closes_issues = mr._meta.get_field(
            'closes_issues').verbose_name
        url = mr._meta.get_field('url').verbose_name
        self.assertEquals(number, 'number')
        self.assertEquals(title, 'title')
        self.assertEquals(repo_id, 'repo id')
        self.assertEquals(repo, 'repo')
        self.assertEquals(author, 'author')
        self.assertEquals(created_at, 'created at')
        self.assertEquals(updated_at, 'updated at')
        self.assertEquals(state, 'state')
        self.assertEquals(hoster, 'hoster')
        self.assertEquals(ci_status, 'ci status')
        self.assertEquals(labels, 'labels')
        self.assertEquals(assignees, 'assignees')
        self.assertEquals(closes_issues, 'closes issues')
        self.assertEquals(url, 'url')

    def test_object_name_is_title(self):
        mr = MergeRequest.objects.get(number=58, repo_id=52889504)
        expected_object_name = 'Removed python 3.3 dependency'
        self.assertEquals(expected_object_name, str(mr))

    def test_many_to_many_field(self):
        mr = MergeRequest.objects.get(number=58, repo_id=52889504)
        label = Label.objects.get(id=1)
        assignee = Contributor.objects.get(login='sks444')
        closes_issue = IssueNumber.objects.get(number=57, repo_id=52889504)

        # Test mr has many to many field with Label
        self.assertEquals(mr.labels.get(pk=label.pk),
                          label)

        # Test mr has many to many field with Contributor
        self.assertEquals(mr.assignees.get(pk=assignee.pk),
                          assignee)

        # Test mr has many to many field with IssueNumber
        self.assertEquals(mr.closes_issues.get(pk=closes_issue.pk),
                          closes_issue)

    def test_get_closes_issues_object(self):
        mr = MergeRequest.objects.get(number=58, repo_id=52889504)
        closes_issues = mr.get_closes_issues_object()

        # Expected closes issue objects list
        issue_objects_list = [
            Issue.objects.get(number=57, repo_id=52889504),
            ]

        # Both the issue objects list should be equal
        self.assertEquals(closes_issues, issue_objects_list)
