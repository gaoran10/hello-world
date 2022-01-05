#!/usr/bin/env python3

import json
import os
import subprocess
import sys

from chaos_mesh_manually import deploy_exp


class ChaosExpManager:

    configuration = {}
    chaos_exps = []
    chaos_exps_params = {}

    def github_api_query_comments(self):
        url = 'https://api.github.com/repos/gaoran10/hello-world/issues/{}/comments?per_page=100'.format(os.getenv('ISSUE_NUMBER'))
        prefix = 'curl -H "Accept: application/vnd.github.v3+json" -u {}:{} '.format(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_TOKEN'))
        proc = subprocess.run(prefix + url, shell=True, capture_output=True)

        return json.loads(proc.stdout.decode('utf-8'))

    def get_chaos_test_configurations(self, comment_body):
        if comment_body.find('== Chaos Cluster Configurations ==') == -1:
            raise RuntimeError("Miss chaos test configuration header.")

        is_config_area = False
        for line in comment_body.splitlines():
            if line.startswith('== Chaos Cluster Configurations =='):
                print('set config area')
                is_config_area = True

            if line.startswith('== Chaos Cluster Configurations End =='):
                print('reach configuration end')
                break

            if not is_config_area or line.count(':') == 0 or line.startswith('#'):
                print('continue line: ', line, is_config_area, line.count(':'), line.startswith('#'))
                continue

            var, val = line.split(':')[0], ':'.join(line.split(':')[1:])
            print('var.strip: ', var.strip())
            if var.strip().startswith('CHAOS_EXP'):
                for exp in val.strip().split(","):
                    self.chaos_exps.append(exp.strip())
                print('chaos exps: ', self.chaos_exps)
            if var.strip().startswith('CHAOS_PARAM'):
                self.chaos_exps_params[var.strip()] = val.strip()

    def get_chaos_exps(self):
        return self.chaos_exps

    def get_chaos_exps_params(self):
        return self.chaos_exps_params

def main():
    if sys.argv.__len__() != 5:
        raise RuntimeError("Miss chaos exp params.")
    exp_type = sys.argv[1]
    if exp_type is None or exp_type == '':
        raise RuntimeError("Miss exp type.")
    component = sys.argv[2]
    if component is None or component == '':
        raise RuntimeError("Miss exp component.")
    properties = sys.argv[3]
    if properties is None or properties == '':
        raise RuntimeError("Miss exp properties.")
    cluster_id = sys.argv[4]
    if cluster_id is None or cluster_id == '':
        raise RuntimeError("Miss exp clusterId.")

#     chaos_exp_manager = ChaosExpManager()
#     comment_body = os.getenv('COMMENT_BODY')

    print('Chaos exp deploy ...')
#     chaos_exp_manager.get_chaos_test_configurations(comment_body)
    exp = {
        "type": exp_type,
        "component": component,
        "properties": json.loads(properties),
        "clusterId": cluster_id
    }
    deploy_exp(exp, './hello/chaos-mesh-template')


main()
