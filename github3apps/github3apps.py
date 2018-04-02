from datetime import datetime, timedelta
import github3
import jwt
import os
import re
import requests
import time


# Used by both the GithubApp and GithubAppInstall classes for pagination.
def get_link_from_response(response):
    if 'Link' in response.headers:
        regex = r"\<https://api.github.com/([^>]*)\>; rel=\"([a-z]*)\""
        groups = re.findall(regex, response.headers['Link'])
        for group in groups:
            if group[1] == 'next':
                return group[1]
    return False


class GithubApp:

    useragent = 'github3apps'

    def __init__(self, appid, pkpath):
        if not os.path.isfile(pkpath):
            raise ValueError('Github Application Key not present')
        self.appid = appid
        self.pkpath = pkpath

    def set_user_agent(self, useragent):
        self.useragent = useragent

    def get_jwt(self):
        with open(self.pkpath, 'r') as keyfile:
            private_key = keyfile.read()

        now = int(time.time())
        payload = {
            # issued at time
            "iat": now,
            # JWT expiration time (10 minute maximum, set to nine in case of crappy clocks)
            "exp": now + (9 * 60),
            # GitHub App's identifier
            "iss": self.appid
        }
        return jwt.encode(payload, private_key, algorithm='RS256').decode("utf-8")

    def request(self, url, method='GET'):
        if method == 'GET':
            requestfunc = requests.get
        elif method == 'POST':
            requestfunc = requests.post
        apptoken = self.get_jwt()

        headers = {
            'Authorization': 'Bearer %s' % (apptoken,),
            'Accept': 'application/vnd.github.machine-man-preview+json',
            'User-Agent': self.useragent
        }
        response = requestfunc('https://api.github.com/%s' % (url,), headers=headers)
        response.raise_for_status()
        retobj = response.json()

        nextpage = get_link_from_response(response)
        if nextpage:
            nextresults = self.request(nextpage)
            retobj += nextresults
        return retobj

    def get_app(self):
        return self.request('app')

    def get_installations(self):
        installs_url = 'app/installations'
        installations = self.request(installs_url)
        return [i['id'] for i in installations]

    def get_installation(self, installation_id):
        return GithubAppInstall(self, installation_id)


# Store login tokens, including expiration, for reuse.
tokens = {}


class GithubAppInstall:

    def __init__(self, app, installid):
        self.app = app
        self.installid = installid

    def get_auth_token(self):
        if self.installid in tokens:
            expiration = tokens[self.installid]['expires_at']
            testtime = datetime.now() - timedelta(minutes=3)
            exptime = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%SZ")
            if exptime > testtime:
                return tokens[self.installid]['token']

        url = "installations/%s/access_tokens" % (self.installid,)
        tokens[self.installid] = self.app.request(url, 'POST')
        return tokens[self.installid]['token']

    def request(self, url):
        client = self.get_github3_client()
        headers = {'Accept': 'application/vnd.github.machine-man-preview+json'}
        res = client._get(url, headers=headers)
        res.raise_for_status()
        return res

    def get_details(self):
        return self.app.request('app/installations/%s' % (self.installid,))

    def get_github3_client(self):
        token = self.get_auth_token()
        gh = github3.login(token=token)
        gh.set_user_agent(self.app.useragent)
        return gh

    def get_repositories(self, url=False):
        if not url:
            url = 'https://api.github.com/installation/repositories'
        res = self.request(url)
        repodata = res.json()
        repos = [repo['full_name'] for repo in repodata['repositories']]

        # Recursively load the next pages, if there are any.
        nextpage = get_link_from_response(res)
        if nextpage:
            repos += self.get_repositories(nextpage)
        return repos

    def get_pr_numbers(self, user, repo):
        repository = self.get_repository(user, repo).repository
        prs = repository.pull_requests(state="open")
        return [pr.number for pr in prs]
