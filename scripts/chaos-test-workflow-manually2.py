#!/usr/bin/env python3

import os
import subprocess
from pom_utils import PomModifier


def update_pom():
    pom_modifier = PomModifier('./pom.xml')
    pulsar_version = os.getenv('PULSAR_VERSION')
    if pulsar_version is not None and pulsar_version != '':
        pom_modifier.update_property('pulsar.version', pulsar_version)
    cloudsmith_api_key = os.getenv('CLOUDSMITH_DEPENDENCY_TOKEN')
    if cloudsmith_api_key is not None and cloudsmith_api_key != '':
        pom_modifier.add_repository('streamnative-staging',
                                    'https://dl.cloudsmith.io/' + cloudsmith_api_key + '/streamnative/staging/maven/',
                                    'true', 'always', 'true', 'always')
    pom_modifier.update_file()


def main():
    test_action = os.getenv('TEST_ACTION')
    server_hook_url = os.getenv('SERVER_HOOK_URL')
    test_id = os.getenv('TEST_ID')
    update_pom()

    if test_action == 'create':
        print('chaos test create ...')

        istio_external_ip = subprocess.os.popen("kubectl get svc -n istio-system | grep ingress | awk '{print$4}'").read().strip()
        print('istio external ip: ', istio_external_ip)
        pulsar_proxy_external_ip = subprocess.os.popen("kubectl get svc -n chaos-" + os.getenv('CLUSTER_ID') + " | grep proxy | awk '{print$4}'").read().strip()
        print('pulsar proxy external ip: ', pulsar_proxy_external_ip)
        pulsar_broker_ingerss_external_ip = subprocess.os.popen("kubectl get svc -n chaos-" + os.getenv('CLUSTER_ID') + " | grep broker-ingress | awk '{print$4}'").read().strip()
        print('pulsar broker external ip: ', pulsar_broker_ingerss_external_ip)

        test_command = os.getenv('TEST_COMMAND')
        test_command += " -Dpulsar.deployment.type=EXTERNAL"
        test_command += " -Dpulsar.external.service.domain=" + pulsar_proxy_external_ip
        test_command += " -Dpulsar.broker-ingerss.external.service.domain=" + pulsar_broker_ingerss_external_ip
        test_command += " -Dchaos.test.duration=" + str(os.getenv('TEST_DURATION'))
        test_command += " -Dchaos.test.id=" + test_id
        test_command += " -Dchaos.test-platform.server=" + server_hook_url

        if os.getenv('TEST_NAME').startswith('KoP'):
            print('start build kop test docker image')
            os.system('cd .. && pwd && ls -al && docker build -t kop-test -f chaos-test/kop-docker/KoPTestDockerfile .')
            print('run kop test based on docker image')

            test_command += " -Dchaos.test.istio.external.ip=chaos-pulsar-" + os.getenv('CLUSTER_ID') + "-broker-0.pulsar.kop.service"
            command = "docker run"
            command += " -e ISTIO_IP=" + istio_external_ip
            command += " -e CLUSTER_ID=" + os.getenv('CLUSTER_ID')
            command += " -e PULSAR_IP=" + pulsar_proxy_external_ip
            command += " -e TEST_COMMAND='" + test_command + "'"
            command += " kop-test"
            print('run kop test command: ', command)
            test_res = os.system(command)
            if test_res != 0:
                raise RuntimeError("Chaos test for kop failed. code " + str(test_res) + ".")
        else:
            command = test_command
            print('run test command: ', command)
            test_res = os.system(command)
            if test_res != 0:
                raise RuntimeError("Chaos test failed. code " + str(test_res) + ".")
    elif test_action == 'finish':
        print('chaos test finish ...')


main()
