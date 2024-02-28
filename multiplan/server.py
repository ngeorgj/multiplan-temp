import json
import requests
import threading
import functools


def run_in_thread(target_function):
    """
    Execute the target instance method in a separate thread.

    :param target_function: The instance method to be executed in the thread.
    """

    @functools.wraps(target_function)
    def wrapper(self, *args, **kwargs):
        def run():
            target_function(self, *args, **kwargs)

        thread = threading.Thread(target=run)
        thread.start()

    return wrapper


class Jira:

    def __init__(self, url):
        self.base_url = url

    pwd = 'NDYxMzI2MDU0NTQxOjiICNpZDPb6r2iLaLR+Y60X8Evb'
    base_url = "https://xxxxxxxxxx.atlassian.net"

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {self.pwd}"
        }

    params = {
        "notifyUsers": False
    }

    def get(self, url, params={}):
        return requests.get(url, params=params, headers=self.headers)

    @run_in_thread
    def delete(self, url, params={}):
        r = requests.delete(url, params=params, headers=self.headers)
        if r.status_code == 429:
            self.delete(url, params)
        else:
            return r

    def post(self, url, data, params={}):
        return requests.post(url, params=params, data=json.dumps(data), headers=self.headers)

    def put(self, url, data, params={}):
        return requests.put(url, params=params, data=json.dumps(data), headers=self.headers)

    @run_in_thread
    def update_issue(self, issuekey, data):
        r = self.put(self.base_url + '/rest/api/2/issue/' + issuekey, {'fields': data, 'update': {}})
        print(r.status_code, r.content)
        if r.status_code == 429:
            return self.update_issue(issuekey, data)
        return r

    @run_in_thread
    def link_issues(self, inwardIssue, outwardIssue, linktype="Associated With"):
        payload = {
            "inwardIssue": {
                "key": inwardIssue
            },
            "outwardIssue": {
                "key": outwardIssue
            },
            "type": {
                "name": linktype
            }
        }
        r = self.post(self.base_url + '/rest/api/2/issueLink', payload)
        print(r.status_code, r.content)
        return r

    def search(self, jql):
        issues = []
        startAt = 0
        while True:
            res = self.get(
                self.base_url + f"/rest/api/2/search",
                params={"jql": jql, "startAt": startAt, "maxResults": 100},
            ).json()
            issues += res["issues"]

            if len(issues) == res["total"]:
                break

            startAt += 100

        return issues


multiplan_server = Jira('http://cyberdeck:8080')


