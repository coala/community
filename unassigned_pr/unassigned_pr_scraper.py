import json
import requests

from github import Github
from django.http import HttpResponse
from gci.config import get_api_key

from community.git import get_org_name


def run(issues, GH_TOKEN, reponame):
    issues_number_list = []
    for j in issues:
        issue_no = j.number
        events = j.get_events()
        data = []
        for i in events:
            if i.commit_id is not None:
                data.append(str(i.commit_id))
        extracted_data = data[-1:]
        if len(extracted_data) == 1:
            commit_id = extracted_data[0]
            url = 'https://api.github.com/search/issues?q='+commit_id + \
                '+type:pr+repo:'+reponame  # Ignore PycodestyleBear (E501)
            r = requests.get(url, headers={'Authentication':
                                           'token '+GH_TOKEN,
                                           'Accept':
                                           'application/vnd.github.symmetra-preview+json'})  # Ignore PycodestyleBear (E501)  and LineLengthBear

            # check commit is a opened as PR or not.
            if r.json()['total_count'] > 0:
                a = r.json()['items'][0]['state']  # check PR is open or closed.
                if a == 'open':
                    # Ignore PycodestyleBear (E501)  and LineLengthBear and InvalidLinkBear
                    url = 'https://api.github.com/repos/'+reponame+'/status/'+commit_id
                    b = requests.get(url, headers={'Authentication':
                                                   'token '+GH_TOKEN})
                    if b.json()['state'] == 'pending' or \
                            b.json()['state'] == 'success':
                        issues_number_list.append(issue_no)

    return issues_number_list


def unassigned_pr_json(request):
    try:
        GH_TOKEN = get_api_key('GH')
    except Exception:
        return HttpResponse('[]')
    g1 = Github(GH_TOKEN)
    org_name = get_org_name()
    org = g1.get_organization(org_name)
    repo = org.get_repo(org_name)
    issues = repo.get_issues()
    issues_list = []
    for myissue in issues:
        if myissue.assignee is None:
            label = []
            for mylabel in myissue.labels:
                label.append(mylabel.name)
            if 'status/blocked' not in label:
                if myissue.state == 'open' and myissue.pull_request is None:
                    issues_list.append(myissue)

    final_list = run(issues_list, GH_TOKEN, repo.full_name)
    return HttpResponse(json.dumps(final_list))
