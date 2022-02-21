#!/usr/bin/env python3

import os
import subprocess


def main():
    test_action = os.getenv('TEST_ACTION')

    if test_action == 'create':
        print('chaos test create ...')

        istio_external_ip = subprocess.os.popen("kubectl get svc -n istio-system | grep ingress | awk '{print$4}'").read().strip()
        print('istio external ip: ', istio_external_ip)
        pulsar_proxy_external_ip = subprocess.os.popen("kubectl get svc -n chaos-" + os.getenv('CLUSTER_ID') + " | grep proxy | awk '{print$4}'").read().strip()
        print('pulsar proxy external ip: ', pulsar_proxy_external_ip)

        if os.getenv('TEST_NAME') == 'KoPTest':
            print('start build kop test docker image')
            os.system('docker build -t kop-test -f chaos-test/kop-docker/KoPTestDockerfile .')
            print('run kop test docker image')
            test_res = os.system('docker run -e istioIP=' + istio_external_ip + ' -e clusterId=' + os.getenv('CLUSTER_ID') + ' -e pulsarIP=' + pulsar_proxy_external_ip + ' kop-test')
            if test_res != 0:
                raise RuntimeError("Chaos test for kop failed. code " + str(test_res) + ".")
        else:
            command = "cd chaos-test && " + os.getenv('TEST_COMMAND')
            command += " -Dpulsar.deployment.type=EXTERNAL"
            command += " -Dpulsar.external.service.domain=" + pulsar_proxy_external_ip
            command += " -Dchaos.test.duration=" + str(os.getenv('TEST_DURATION'))
            command += " -Dchaos.test.istio.external.ip=" + istio_external_ip
            print('run test command: ', command)
            test_res = os.system(command)
            if test_res != 0:
                raise RuntimeError("Chaos test failed. code " + str(test_res) + ".")
    elif test_action == 'finish':
        print('chaos test finish ...')

main()
