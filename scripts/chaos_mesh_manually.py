import json
import random
import os
import sys

from ruamel.yaml import YAML

# pip install ruamel.yaml


class ChaosMeshEditor:

    base_ns_name = 'chaos-'

    def __init__(self, issue_number, input_file_path, is_scheduled=False):
        self._issue_number = issue_number
        self._is_scheduled = is_scheduled
        self._ns = self.base_ns_name + str(issue_number)
        self._exp = self.load_file(input_file_path)
        self._output_file_path = './' + self._exp['metadata']['name'] + ".yaml"

    def load_file(self, input_file_path):
        file = open(input_file_path, 'r', encoding="utf-8")
        yaml=YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
        exp = yaml.load(file)
        if self._is_scheduled:
            exp['metadata']['name'] = exp['metadata']['name'] + '-' + str(self._issue_number) + "-scheduled"
        else:
            exp['metadata']['name'] = exp['metadata']['name'] + '-' + str(self._issue_number) + '-' + self.random_name(5)
        exp['metadata']['namespace'] = self._ns
        return exp

    def write(self):
        print('------ write experiment file ------')
        print(self._exp)
        output = open(self._output_file_path, 'w', encoding="utf-8")
        yaml=YAML()
        yaml.default_flow_style = False
        yaml.dump(self._exp, output)

    def deploy(self):
        self.write()
        os.system('cat ' + self._output_file_path)
        # os.system('kubectl apply -f ' + self._output_file_path)
        print('deploy file ', self._output_file_path)

    def add_label_selector(self, component):
        if self._is_scheduled:
            exp_type = self._exp['spec']['type']
            exp_type = self.format_exp_type(exp_type)
            self._exp['spec'][exp_type]['selector']['namespaces'] = [self._ns]
            self._exp['spec'][exp_type]['selector']['labelSelectors']['component'] = component
        else:
            self._exp['spec']['selector']['namespaces'] = [self._ns]
            self._exp['spec']['selector']['labelSelectors']['component'] = component

    def set_schedule(self, corn):
        if not self._is_scheduled:
            raise RuntimeError("Setting schedule only support scheduled experiments.")
        self._exp['spec']['schedule'] = corn

    def format_exp_type(self, exp_type):
        type_char_list = list(exp_type)
        type_char_list[0] = type_char_list[0].lower()
        return ''.join(type_char_list)

    def random_name(self, count):
        str = 'abcdefghijklmnopqrstuvwxyz0123456789'
        random_str = ''
        for i in range(count):
            random_str += random.choice(str)
        return random_str


def deploy_exp(base_path="../chaos-mesh-template"):
    if sys.argv.__len__() != 2:
        raise RuntimeError("Miss chaos exp params.")
    exp_list_json = sys.argv[1]
    if exp_list_json is None or exp_list_json == '':
        raise RuntimeError("Miss exp list json string.")

    print('deploy exp: ', exp_list_json)
    exp_list = json.loads(exp_list_json);
    if not exp_list:
        raise RuntimeError("No chaos-mesh experiments.")

    for exp in exp_list:
        if exp['expType'] == 'POD_KILL':
            editor = ChaosMeshEditor(exp['clusterId'], base_path + '/pod-kill-schedule-temp.yaml', True)
            editor.add_label_selector(exp['component'])
            if 'cron' in exp['properties']:
                editor.set_schedule(exp['properties']['cron'])
            else:
                editor.set_schedule('*/5 * * * *')
            editor.deploy()
        elif exp['expType'] == 'NETWORK_DELAY':
            editor = ChaosMeshEditor(exp['clusterId'], base_path + '/pod-network-delay-schedule-temp.yaml', True)
            editor.add_label_selector(exp['component'])
            if 'cron' in exp:
                editor.set_schedule(exp['properties']['cron'])
            else:
                editor.set_schedule('*/5 * * * *')
            editor.deploy()


deploy_exp()