import json
import requests
import sys

from ruamel.yaml import YAML


def format_exp_type(exp_type):
    type_char_list = list(exp_type)
    type_char_list[0] = type_char_list[0].lower()
    return ''.join(type_char_list)


def check_and_get_configuration(configuration, configuration_name):
    if configuration_name not in configuration or configuration[configuration_name] is None \
            or configuration[configuration_name] == '':
        if configuration_name == 'enableKoP':
            return False
        if configuration_name == 'enableMoP':
            return False
        if configuration_name == 'brokerEnv':
            return []
        raise RuntimeError("Miss cluster configuration " + str(configuration_name))
    return configuration[configuration_name]


def check_image_user(image_name, image_version):
    url = 'https://hub.docker.com/v2/repositories/' + image_name + '/tags/' + image_version + '/images'
    r = requests.get(url)
    for layer in r.json()[0]['layers']:
        if str(layer['instruction']).__contains__('USER 10000'):
            print('contain USER 10000')
            return True
    return False


class ValuesEditor:
    base_ns_name = 'chaos-'

    def __init__(self, input_file_path):
        self._values = self.load_file(input_file_path)
        self._output_file_path = input_file_path + '-u'

    @staticmethod
    def load_file(input_file_path):
        file = open(input_file_path, 'r', encoding="utf-8")
        yaml = YAML(typ='safe')  # default, if not specified, is 'rt' (round-trip)
        values = yaml.load(file)
        return values

    def check_values(self):
        print('------------ values ------------')
        print(self._values)

    def write(self):
        output = open(self._output_file_path, 'w', encoding="utf-8")
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.dump(self._values, output)

    # def deploy(self):
    #     self.write()
    #     os.system('cat ' + self._output_file_path)
    #     os.system('kubectl apply -f ' + self._output_file_path)
    #     print('deploy file ', self._output_file_path)

    def update(self, json_update):
        pass

    def get_values(self):
        return self._values


def deploy_exp():
    if sys.argv.__len__() != 3:
        raise RuntimeError("Miss chaos exp params.")
    values_file_path = sys.argv[1]
    if values_file_path is None or values_file_path == '':
        raise RuntimeError("Miss param values file path.")
    cluster_configuration_json = sys.argv[2]
    if cluster_configuration_json is None or cluster_configuration_json == '':
        raise RuntimeError("Miss param cluster configuration json.")

    cluster_configuration = json.loads(cluster_configuration_json)
    print('cluster configuration: ', cluster_configuration)
    if cluster_configuration is None:
        raise RuntimeError("No cluster configuration.")

    # /Volumes/shit/Workspaces/GitHub/charts/charts/pulsar-2.8.0.8/values.yaml
    values_editors = ValuesEditor(input_file_path=values_file_path)
    values = values_editors.get_values()

    image_name = check_and_get_configuration(cluster_configuration, 'imageName')
    image_version = check_and_get_configuration(cluster_configuration, 'imageVersion')

    image_version_list = ['zookeeper', 'bookie', 'autorecovery', 'presto', 'presto_worker', 'broker', 'proxy',
                          'pulsar_detector', 'functions']
    image_list = ['broker', 'pulsar_detector', 'functions']
    for image in values['images']:
        if image in image_version_list:
            values['images'][image]['tag'] = image_version
        if image in image_list:
            values['images'][image]['repository'] = image_name

    values['components']['kop'] = check_and_get_configuration(cluster_configuration, 'enableKoP')

    broker_env = check_and_get_configuration(cluster_configuration, 'brokerEnv')
    for env in broker_env:
        values['broker']['extraEnv'].append({
            'name': env,
            'value': broker_env[env]
        })

    if check_image_user(image_name, image_version):
        print('USER 10000 exist')
        values['zookeeper']['securityContext'] = {
            'runAsUser': 10000,
            'runAsGroup': 0,
            'fsGroup': 0
        }
    else:
        values['zookeeper']['securityContext'] = {}
    print(values['zookeeper']['securityContext'])

    values_editors.check_values()
    values_editors.write()


deploy_exp()
