#!/usr/bin/env python3

import os
import json
import subprocess


class ChaosTestManager:

    configuration = {}

    def github_api_query_comments(self):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments?per_page=100'.format(os.getenv('ISSUE_NUMBER'))
        prefix = 'curl -H "Accept: application/vnd.github.v3+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        proc = subprocess.run(prefix + url, shell=True, capture_output=True)

        return json.loads(proc.stdout.decode('utf-8'))

    def get_chaos_test_configurations(self, comments):
        lasthead = None
        for comment in comments:
            if comment['body'].startswith('== Chaos Test Arguments Header =='):
                lasthead = comment['body']

        if not lasthead:
            print('The arguments not generated yet')
            return

        for line in lasthead.splitlines():
            if not line.count(':'):
                continue

            var, val = line.split(':')[0], ':'.join(line.split(':')[1:])

            self.configuration[var] = val

    def link_action_with_issue(self):
        print('link_action_with_issue action: ', os.getenv('ACTION'))

def main():
    chaos_test_manager = ChaosTestManager()
    comments = chaos_test_manager.github_api_query_comments()
    chaos_test_manager.get_chaos_test_configurations(comments)
    print('configurations: ', chaos_test_manager.configuration)
    link_action_with_issue()

main()
