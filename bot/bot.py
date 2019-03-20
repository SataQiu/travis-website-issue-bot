from github import Github
import time
import os


def getRefPr(issue):
    ref_pr_str = ""
    issue_comments = issue.get_comments()
    for issue_comment in issue_comments:
        if "kubernetes/website#" in issue_comment.body:
            ref_pr_str = issue_comment.body
    if len(ref_pr_str) != 0:
        ref_pr_str = ref_pr_str.strip()
        pr_num_str = ref_pr_str.split('#')[-1]
        try:
            pr_num = int(pr_num_str)
        except ValueError:
            print("input %s is not a int." % pr_num_str)
        return pr_num
    return -1


def hasPushedComment(issue):
    issue_comments = issue.get_comments()
    for issue_comment in issue_comments:
        if "/pushed" in issue_comment.body:
            return True
    return False


def createPushedComment(issue):
    issue.create_comment("/pushed")


def createMergedComment(issue):
    issue.create_comment("/merged")


if __name__ == "__main__":

    g = Github(os.environ.get('GITHUB_TOKEN'))

    task_repo = g.get_repo("k8smeetup/website-tasks")
    website_repo = g.get_repo("kubernetes/website")

    open_issues = task_repo.get_issues(state='open', assignee="SataQiu")

    for issue in open_issues:
        print(issue)
        if not hasPushedComment(issue):
            if getRefPr(issue) != -1:
                createPushedComment(issue)
                time.sleep(2)
        if hasPushedComment(issue):
            pr_num = getRefPr(issue)
            if pr_num != -1:
                pull = website_repo.get_pull(pr_num)
                if pull.merged:
                    createMergedComment(issue)
    print("Done!")
