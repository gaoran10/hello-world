#!/usr/bin/env python3

import os
import json
import subprocess
import requests
from requests.auth import HTTPBasicAuth

class ChaosClusterManager:

    configuration = {}

    def github_api_query_comments(self):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments?per_page=100'.format(os.getenv('ISSUE_NUMBER'))
        prefix = 'curl -H "Accept: application/vnd.github.v3+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        proc = subprocess.run(prefix + url, shell=True, capture_output=True)

        return json.loads(proc.stdout.decode('utf-8'))

    def load_configurations(self, comment_body):
        if comment_body.find('== Chaos Cluster Configurations ==') == -1:
            raise RuntimeError("Miss chaos cluster configuration header.")

        is_config_area = False
        for line in comment_body.splitlines():
            if line.startswith('== Chaos Cluster Configurations =='):
                is_config_area = True

            if not is_config_area or not line.count(':') or not line.startswith('#'):
                continue
            elif line.startswith('== Chaos Cluster Configurations End =='):
                break

            var, val = line.split(':')[0], ':'.join(line.split(':')[1:])
            os.environ['CHAOS_CLUSTER_' + var.strip()] = val.strip()
            print('add chaos cluster configuration in env. ', 'CHAOS_CLUSTER_' + var.strip(), '=', os.getenv('CHAOS_CLUSTER_' + var.strip()))

        if os.getenv('CHAOS_CLUSTER_IMAGE_VERSION') is None or os.getenv('CHAOS_CLUSTER_IMAGE_VERSION') == '':
            raise RuntimeError("Need to set the `streamnative/pulsar-all` image version.")

    def github_api_update_issue(self, issue_number, body):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}'.format(issue_number)

        headers = {'Accept': 'application/vnd.github.v3+json'}
        auth = HTTPBasicAuth(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        result = requests.patch(url, headers=headers, auth=auth, json={"body": body})
        print('update result: ', result)

    def github_api_get_issue(self, issue_number):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}'.format(issue_number)

        headers = {'Accept': 'application/vnd.github.v3+json'}
        auth = HTTPBasicAuth(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        result = requests.get(url, headers=headers, auth=auth)
        return result.json()

    def link_action_with_issue(self, issue_number, test_action, old_body):
        body = old_body
        body += '\r\n \r\n'
        body += '-------------- \r\n'
        body += 'action: {} \r\n'.format(test_action)

        if test_action == 'finish':
            body += 'status: {} \r\n'.format(os.getenv('STATUS'))
        elif test_action == 'create':
            body += 'https://github.com/gaoran10/hello-world/actions/runs/' + os.getenv('RUN_ID')

        print('link_action_with_issue body: ', body)
        self.github_api_update_issue(issue_number, body)

def main():
    chaos_cluster_manager = ChaosClusterManager()
    test_action = os.getenv('TEST_ACTION')
    comment_body = os.getenv('COMMENT_BODY')
    issue_number = os.getenv('ISSUE_NUMBER')

    if test_action == 'create':
        print('chaos cluster initialization start ...')
        chaos_cluster_manager.load_configurations(comment_body)
        chaos_cluster_manager.link_action_with_issue(issue_number, test_action, comment_body)
        res = os.system('./scripts/pulsar/change_pulsar_image.sh ' + os.getenv('CHAOS_CLUSTER_IMAGE_VERSION'))
        print('change chart Pulsar image res ', res)
    elif test_action == 'finish':
        print('chaos cluster initialization finish ...')
        comment = chaos_cluster_manager.github_api_get_issue(issue_number)
        chaos_cluster_manager.link_action_with_issue(issue_number, test_action, comment['body'])
main()
