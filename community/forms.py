from django import forms


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
