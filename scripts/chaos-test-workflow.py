#!/usr/bin/env python3

import os
import json
import subprocess
import requests
from requests.auth import HTTPBasicAuth

class ChaosTestManager:

    configuration = {}

    def github_api_query_comments(self):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments?per_page=100'.format(os.getenv('ISSUE_NUMBER'))
        prefix = 'curl -H "Accept: application/vnd.github.v3+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        proc = subprocess.run(prefix + url, shell=True, capture_output=True)

        return json.loads(proc.stdout.decode('utf-8'))

    def get_chaos_test_configurations(self, comment_body):
        configuration_body = None
        if comment_body.startswith('== Chaos Test Configurations =='):
            configuration_body = comment_body

        if not configuration_body:
            print('The arguments not generated yet')
            return

        json_str = ''
        for line in configuration_body.splitlines():
            if line.startswith('== Chaos Test Configurations =='):
                continue
            elif line.startswith("```json"):
                continue
            elif line.startswith("```"):
                break
            else:
                json_str += line
        print('get chaos test json_str: ', json_str)
        config = json.loads(json_str)
        print('get chaos test config: ', config)
        return config

    def github_api_create_comment(self, number, body):
        body = body.replace('\n', '\\n')
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments'.format(number)
        prefix = 'curl -H "Accept: application/vnd.github.v3.text+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        param = ' -d \'{"body": "' + body + '"}\''

        proc = subprocess.run(prefix + url + param, shell=True, capture_output=True)
        return json.loads(proc.stdout.decode('utf-8'))

    def github_api_update_comment(self, comment_id, body):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/comments/{}'.format(comment_id)

        headers = {'Accept': 'application/vnd.github.v3+json'}
        auth = HTTPBasicAuth(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        result = requests.patch(url, headers=headers, auth=auth, json={"body": body})
        print('update result: ', result)

    def github_api_get_comment(self, comment_id):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/comments/{}'.format(comment_id)

        headers = {'Accept': 'application/vnd.github.v3+json'}
        auth = HTTPBasicAuth(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        result = requests.get(url, headers=headers, auth=auth)
        return result.json()

    def link_action_with_issue(self, comment_id, test_action, old_comment_body):
        body = old_comment_body
        body += '\r\n \r\n'
        body += '-------------- \r\n'
        body += 'action: {} \r\n'.format(test_action)

        if test_action == 'finish':
            body += 'status: {} \r\n'.format(os.getenv('STATUS'))
        elif test_action == 'create':
            body += 'https://github.com/gaoran10/hello-world/actions/runs/' + os.getenv('RUN_ID')

        print('link_action_with_issue body: ', body)
        self.github_api_update_comment(comment_id, body)

def main():
    chaos_test_manager = ChaosTestManager()
    test_action = os.getenv('TEST_ACTION')
    comment_body = os.getenv('COMMENT_BODY')
    comment_id = os.getenv('COMMENT_ID')

    if test_action == 'create':
        print('chaos test create ...')
        chaos_test_manager.get_chaos_test_configurations(comment_body)
        chaos_test_manager.link_action_with_issue(comment_id, test_action, comment_body)
    elif test_action == 'finish':
        print('chaos test finish ...')
        comment = chaos_test_manager.github_api_get_comment(comment_id)
        chaos_test_manager.link_action_with_issue(comment_id, test_action, comment['body'])
main()
