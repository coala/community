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
