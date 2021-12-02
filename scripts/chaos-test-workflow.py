#!/usr/bin/env python3

import os
import json
import subprocess
import requests
from requests.auth import HTTPBasicAuth

import chaos_mesh import deploy_exps

class ChaosTestManager:

    configuration = {}
    chaos_exps = []

    def github_api_query_comments(self):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments?per_page=100'.format(os.getenv('ISSUE_NUMBER'))
        prefix = 'curl -H "Accept: application/vnd.github.v3+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        proc = subprocess.run(prefix + url, shell=True, capture_output=True)

        return json.loads(proc.stdout.decode('utf-8'))

    def get_chaos_test_configurations(self, comment_body):
        if comment_body.find('== Chaos Test Configurations ==') == -1:
            raise RuntimeError("Miss chaos test configuration header.")

        is_config_area = False
        for line in comment_body.splitlines():
            if line.startswith('== Chaos Test Configurations =='):
                print('set config area')
                is_config_area = True

            if line.startswith('== Chaos Test Configurations End =='):
                print('reach configuration end')
                break

            if not is_config_area or line.count(':') == 0 or line.startswith('#'):
                print('continue line: ', line, is_config_area, line.count(':'), line.startswith('#'))
                continue

            var, val = line.split(':')[0], ':'.join(line.split(':')[1:])
            os.environ['CHAOS_TEST_' + var.strip()] = val.strip()
            print('add chaos test configuration in env. ', 'CHAOS_TEST_' + var.strip(), '=', os.getenv('CHAOS_TEST_' + var.strip()))
            if var.strip() == 'CHAOS_EXPS':
                for exp in val.strip().split(",")
                    self.chaos_exps.append(exp.strip())
            print('chaos exps: ', self.chaos_exps)

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

    def get_chaos_exps(self):
        return self.chaos_exps

def main():
    chaos_test_manager = ChaosTestManager()
    test_action = os.getenv('TEST_ACTION')
    comment_body = os.getenv('COMMENT_BODY')
    comment_id = os.getenv('COMMENT_ID')

    if test_action == 'create':
        print('chaos test create ...')
        chaos_test_manager.get_chaos_test_configurations(comment_body)
        chaos_test_manager.link_action_with_issue(comment_id, test_action, comment_body)
        deploy_exps(chaos_test_manager.get_chaos_exps(), './hello/chaos-mesh-template')
    elif test_action == 'finish':
        print('chaos test finish ...')
        comment = chaos_test_manager.github_api_get_comment(comment_id)
        chaos_test_manager.link_action_with_issue(comment_id, test_action, comment['body'])
main()
