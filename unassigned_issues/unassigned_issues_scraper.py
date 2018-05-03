import json

from django.http import HttpResponse
from gci.config import get_api_key
from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubRepository import GitHubRepository
from IGitt.Interfaces import MergeRequestStates
from IGitt.Interfaces import IssueStates
from IGitt.Interfaces.CommitStatus import Status

from community.git import get_org_name


def run(mr_requests):
    issues_number_list = []
    for pr in mr_requests:
        if pr.state is MergeRequestStates.OPEN:
            for commit in pr.commits:
                status = commit.combined_status
                break
            if status in [Status.PENDING, Status.SUCCESS]:
                for issue in pr.closes_issues:
                    if issue.state is IssueStates.OPEN:
                        if pr.author.username not in (
                                [a.username for a in issue.assignees]):
                            issues_number_list.append(issue.number)
    issues_number_list.sort()
    return issues_number_list


def unassigned_issues_activity_json(request):
    try:
        GH_TOKEN = get_api_key('GH')
    except Exception:
        return HttpResponse('[]')
    org_name = get_org_name()
    org_repo_name = org_name
    # Here 'org_repo_name' is the name of repository of a organization.
    # (assumed here, that name of repository is same as the organization name.)
    # But you can change 'org_repo_name' as per your requirement.
    repo_name = org_name + '/' + org_repo_name
    # 'repo_name' is a full name of repository e.g. `fossasia/susi_server`
    # which further used for query (assuming here 'org_name' is different from
    # 'org_repo_name')
    repo = GitHubRepository(GitHubToken(GH_TOKEN), repo_name)
    mr_requests = repo.merge_requests
    final_list = run(mr_requests)
    return HttpResponse(json.dumps(final_list))
