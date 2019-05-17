#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import namedtuple


Issue = namedtuple('Issue', ['issue_id', 'title'])


class GitService:

    user = None

    def __init__(self):
        from github import Github
        if GitService.user is None:
            conn = Github()
            GitService.user = conn.get_user('pythoncanarias')

    def list_repos(self) -> list:
        """List the names of all the public repositories.
        """
        return [r.name for r in self.user.get_repos()]

    def list_issues(self, repo_name: str) -> list:
        repo = GitService.user.get_repo(repo_name)
        result = [
            Issue(issue_id=i.number, title=i.title)
            for i in repo.get_issues()
            ]
        return result
