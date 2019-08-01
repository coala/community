from datetime import datetime

from django import forms

from community.git import get_org_name

TODAY = datetime.now().today()
ORG_NAME = get_org_name()


class JoinCommunityForm(forms.Form):

    github_username = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Make sure to NOT enter your github profile url',
                'autocomplete': 'off'
            }
        )
    )
    gh_first_repo = forms.URLField(
        required=False, label='GitHub Personal Repository',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'A valid github url of your personal repository',
                'autocomplete': 'off'
            }
        )
    )
    gh_git_training_exercise = forms.URLField(
        required=False, label='From which GitHub repository you have done git'
                              ' training?',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'A valid github url of git training repository',
                'autocomplete': 'off'
            }
        )
    )
    gh_most_contributed_repo = forms.URLField(
        required=False,
        label="GitHub Repository to which you've contributed most!",
        widget=forms.URLInput(
            attrs={
                'placeholder': 'A valid github public repository url',
                'autocomplete': 'off'
            }
        )
    )

    gitlab_user_id = forms.IntegerField(
        label='GitLab User ID',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Make sure to NOT enter your gitlab profile url',
                'autocomplete': 'off'
            }
        )
    )
    gl_first_repo_id = forms.IntegerField(
        required=False, label='GitLab Personal Project ID',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Your personal gitlab project ID',
                'autocomplete': 'off'
            }
        )
    )
    gl_git_training_exercise = forms.IntegerField(
        required=False, label='From which GitLab project you have done git'
                              ' training?',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'A valid project ID of Git training project',
                'autocomplete': 'off'
            }
        )
    )
    gl_most_contributed_repo_id = forms.IntegerField(
        required=False,
        label="GitLab Project to which you've contributed most!",
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'A valid ID of gitlab public project',
                'autocomplete': 'off',
            }
        )
    )


class CommunityGoogleForm(forms.Form):
    user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    title = forms.CharField(
        max_length=100, label='Title',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    description = forms.CharField(
        max_length=1000, label='Form Description', required=False,
        widget=forms.Textarea(attrs={'autocomplete': 'off'})
    )
    url = forms.URLField(
        label='Google Form URL',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    expiry_date = forms.DateTimeField(
        label='Expiry date and time', required=False,
        help_text='DateTime Format should be YYYY-MM-DD HH:MM:SS',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )


class CommunityEvent(forms.Form):
    user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    title = forms.CharField(
        max_length=300, label='Event Title',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    description = forms.CharField(
        max_length=1000, label='Event Description', required=False,
        widget=forms.Textarea(attrs={'autocomplete': 'off'})
    )
    start_date_time = forms.DateTimeField(
        label='Event occurrence date and time(in UTC)',
        help_text='DateTime Format should be YYYY-MM-DD HH:MM:SS',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    end_date_time = forms.DateTimeField(
        label='Event end date and time(in UTC)', required=False,
        help_text='DateTime Format should be YYYY-MM-DD HH:MM:SS',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )


class OrganizationMentor(forms.Form):
    user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    year = forms.ChoiceField(
        choices=[(TODAY.year, TODAY.year), (TODAY.year + 1, TODAY.year + 1)],
        label='Mentoring Year', widget=forms.Select()
    )
    program = forms.ChoiceField(
        choices=[('GSoC', 'Google Summer of Code'), ('GCI', 'Google Code-In')],
        label='Mentoring Program'
    )


class GSOCStudent(forms.Form):
    user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    year = forms.IntegerField(
        label='Participation year',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    project_topic = forms.CharField(
        max_length=300, label='GSoC Project Topic',
        help_text='Should be same as on GSoC Website!',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    project_desc = forms.CharField(
        max_length=2000, label='Project Description',
        widget=forms.Textarea(attrs={'autocomplete': 'off'})
    )
    accepted_proposal = forms.URLField(
        label='Accepted Proposal URL',
        help_text='The proposal you submitted during GSoC Program!',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    cEP = forms.URLField(
        label='Org Enhancement Proposal Merge Request', required=False,
        help_text='For example, in {org} we have cEP({org} Enhancement '
                  'Proposal)'.format(org='coala'),  # Ignore KeywordBear
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    project_url = forms.URLField(
        label='GSoC Project URL',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    mentors = forms.CharField(
        max_length=200, label='Project Mentors',
        help_text='Separate name of mentor by comma(,)',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    image = forms.URLField(
        label='Personal Image URL', required=False,
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )


class AssignIssue(forms.Form):
    user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    hoster = forms.ChoiceField(
        choices=[('github', 'GitHub'), ('gitlab', 'GitLab')], label='Hoster'
    )
    repository_url = forms.URLField(
        label='Repository URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community/',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    issue_number = forms.IntegerField(
        label='Issue Number',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    requested_user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'hidden': True})
    )


class NewcomerPromotion(forms.Form):
    github_username = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    gitlab_user_id = forms.IntegerField(
        label='GitLab User ID',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    project_web_url = forms.URLField(
        label='Personal Project URL',
        help_text="A project in which you've added .coafile and build it!",
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    build_file_relative_path = forms.CharField(
        label='Build File',
        help_text='For example, if integrated Travis CI, provide '
                  '/relative/path/to/travis.yml',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    coafile_relative_path = forms.CharField(
        label='.coafile File',
        help_text="Add 5 or more sections in '.coafile'! Provide "
                  '/relative/path/to/.coafile',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    gist_or_snippet_id = forms.IntegerField(
        label='Gist or Snippet ID',
        help_text='Paste your local build output to gist or snippet! Choose '
                  'Gist, if personal project on GitHub else choose '
                  'GitLab Snippet.',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )
    newcomer_solved_issue_web_url = forms.URLField(
        label='Issue URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community/'
                  'issues/1',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    newcomer_issue_related_pr = forms.URLField(
        label='Merge Request URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community'
                  '/pulls/1',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    newcomer_issue_pr_reviewed_url = forms.URLField(
        label='Reviewed PR URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community/'
                  'pulls/2',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    low_level_solved_issue_web_url = forms.URLField(
        label='Issue URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community/'
                  'issues/1',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    low_level_issue_related_pr = forms.URLField(
        label='Merge Request URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community'
                  '/pulls/1',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    low_level_issue_pr_reviewed_url = forms.URLField(
        label='Reviewed PR URL',
        help_text=f'For example, https://github.com/{ORG_NAME}/community/'
                  'pulls/2',
        widget=forms.URLInput(attrs={'autocomplete': 'off'})
    )
    request_created_by_user = forms.CharField(
        max_length=50, label='GitHub Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'hidden': True})
    )


class Feedback(forms.Form):
    username = forms.CharField(
        label='GitHub Username', required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    feedback = forms.CharField(
        max_length=1000, label='Feedback',
        widget=forms.Textarea(attrs={'autocomplete': 'off'})
    )
    experience = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'hidden': True})
    )
