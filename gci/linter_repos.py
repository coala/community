from multiprocessing import Pool

import giturlparse

from community.git import get_irepo


def simplify_issue(issue, repo_url=''):
    return {
      'id': issue.number,
      'repo_url': repo_url,
      'title': issue.title,
      'labels': list(issue.labels),
      'description': issue.description,
    }


def _lower_set(iterable):
    return set(map(str.lower, iterable))


def issue_filter(issue, labels, desc_keywords):
    norm_issue_labels = _lower_set(issue['labels'])
    norm_labels = _lower_set(labels)

    if len(norm_issue_labels & norm_labels) > 0:
        return True

    norm_keywords = _lower_set(desc_keywords)
    norm_text = str.lower(issue['title'] + ' ' + issue['description'])
    norm_text = set(norm_text.split())

    if len(norm_keywords & norm_text) > 0:
        return True

    return False


def fetch_issues(targets, labels=[], desc_keywords=[],
                 processes=8, debug=False):
    all_repo_issues = dict()

    for target in targets:
        if debug:
            print('processing', target)

        parsed_url = giturlparse.parse(target)
        repo = get_irepo(parsed_url)

        with Pool(processes=processes) as pool:
            all_issues = pool.map(simplify_issue, repo.issues)

        for issue in all_issues:
            issue['repo_url'] = target

        repo_issues = {
            'all': all_issues,
            'filtered': list(filter(
                lambda issue: issue_filter(issue, labels, desc_keywords),
                all_issues)),
        }

        all_repo_issues[parsed_url.href] = repo_issues

    return all_repo_issues
