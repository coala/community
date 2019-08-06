# community

![Header](/docs/_static/images/header.png)

## About

The repository generates an *open-source community* static website, using the
publicly available information about contributors and the organization. The
information used is fetched from the **Webservices API**.

**Features:**
  1. Creates a *static django website* using *django_distill*.
  2. Community data is being fetched from an API, named Webservices
    *(on GitLab)*. To use it, just **fork** the repository, and Change the
     organization name in *settings.py* file.
  3. Uses the  [GCI private API](https://developers.google.com/open-source/gci/resources/downloads/TaskAPISpec.pdf)
     to fetch information about students who participated in Google Code-In
     with the organization.
  4. Uses IGitt, supporting both GitHub & GitLab
  5. __Attention:__ This repository only re-publishes publicly available
    information.

## Environment variables used

1. **``GH_TOKEN``**: A *GitHub Personal Access Token*, which can be generated
 from your *account settings* under the **Developer Settings**.
2. **``GL_TOKEN``**: A *GitLab Personal Access Token*, which can be generated
 from your *account settings* under the tab **Access Tokens**.
3. **``OH_TOKEN``**: An *OpenHub Personal Access Token*, which can be
 generated from your *account settings*.

## Netlify based Community Forms
1. **``OSFORMS_NETLIFY_FORM_NAME``**: A form which receives submission
    from community *developers*, if they want to share any open-source form
    like a Google Doc which is to be shared with all developers or within
    the community.
2. **``CALENDAR_NETLIFY_FORM_NAME``**: A form which receives submission
    from community *developers*, if they want to add an upcoming event like
    project related events, software releases, survey result announcements
    etc.
3. **``MENTOR_FORM_NAME``**: A form which receives submission from
    community *developers*, if they want to participate as an
    organization mentor, who will be available to mentor projects in the
    summer/winter programs like Google Summer of Code, Google Code-In etc.
4. **``GSOC_STUDENT_FORM_NAME``**: A form which receives submission from
    community *newcomers & developers*, if they had participated with the
    organization in Google Summer of Code and completed the proposed
    project.
5. **``ISSUES_ASSIGN_REQUEST_FORM_NAME``**: Any contributor, who wishes to work
    on an issue can fill-up this form and request to get assigned on that
    issue.
6. **``NEWCOMER_PROMOTION_REQUEST_FORM_NAME``**: Any newcomer who wishes to get
    the **Developer Role** in th oragnization, can fill-up the form and request
    the access.
7. **``FEEDBACK_FORM_NAME``**: The name is self-understandable :innocent:

__ATTENTION DEVs:__ To use the forms, set the above mentioned environment
 variables. All the forms, have respective **cron-jobs** defined in
 **Webservices**, which processes the contributor request and check if the
 request is valid or not. If not valid request, the user will be sent an
 email informing about the validation errors.

## Deploy your fork on Netlify:

Following are the steps to deploy your forked *community* repository on Netlify:

1. Signup on [netlify](https://app.netlify.com/).
2. Click on **New site from Git**.
3. Choose the **Git provider** as *Github* and Choose your forked *community*
repository, named **< username>/community**.
4. Further, choose **master** branch to deploy and set the following *Basic*
 *build settings*:
    * Set Build command to **.ci/build.sh**.
    * Set Publish directory to **public**.
    * Click on **Show advanced** and add a **New variable** by choosing the
     option. After that, add the **required Environment variables** according
     to your need.
    * **Note:** ``GH_TOKEN`` is a required environment variable, and you must
    set that before your deploy the site.
5. Click on **Deploy Site** to deploy the site.

## Want to add Netlify OAuth (GitHub and GitLab)?

The repository has already integrated Netlify OAuth, all is to be done is
to register new GitHub and GitLab OAuth apps on your account. So, that the
OAuth is set to working on your fork.

For registering a new GitHub OAuth App, you can follow-up the [Netlify OAuth
 Provider Documentation](https://www.netlify.com/docs/authentication-providers/).

For registering a new GitLab OAuth App,
1. Go to your account Settings, and click *Applications* under
 the Settings (or use this [shortcut](https://gitlab.com/profile/applications)).
2. After page opens, you will see a form for registering a new OAuth
 application.
3. Enter the *name of the Application*.
4. For the Redirect URI, enter ``https://api.netlify.com/auth/done``.
5. And, the last one is the most important field, which is the **Scopes**. Set
 it according to your needs. This repository uses ***api*** scope. If you
 choose a different scope other than the ***api***, make sure to change it in
 the `static/js/main.js` JavaScript file.
