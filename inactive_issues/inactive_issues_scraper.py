import time
import json

from github import Github
from dateutil.parser import parse
from datetime import date
from django.http import HttpResponse
from gci.config import get_api_key

from community.git import get_org_name


def run(issues):
    issues_number_list = []
    for j in issues:
        issue_no = j.number
        events = j.get_events()
        myevent_list = []
        data = []
        for i in events:
            myevent_list.append(str(i.event))
        for i in events:
            if i.commit_id is not None:
                data.append(str(i.created_at))
        for i, myevents in reversed(list(enumerate(myevent_list))):
            if myevents == 'unassigned':
                break
            elif myevents == 'assigned':
                a = events[i].created_at
                c = (date.fromtimestamp(time.time()) - a.date()).days
                if c >= 60:  # for checking assigned duration

                    mydata = list(reversed(data))
                    if len(mydata) != 0:
                        commit1 = parse(mydata[0])
                        calculated_days = (date.fromtimestamp(
                            time.time()) - commit1.date()).days
                        if calculated_days >= 60:
                            # for checking last commit update
                            issues_number_list.append(issue_no)
                    else:
                        issues_number_list.append(issue_no)
                break
    return issues_number_list


def inactive_issues_json(request):
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
        labels = []
        for mylabel in myissue.labels:
            labels.append(mylabel.name)
        if 'status/blocked' not in labels:
            if myissue.state == 'open' and myissue.pull_request is None:
                issues_list.append(myissue)

    final_list = run(issues_list)
    return HttpResponse(json.dumps(final_list))
