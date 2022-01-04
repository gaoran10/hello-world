#!/usr/bin/env python3

import os
import json
import subprocess
import requests
from chaos_mesh import deploy_exps
from requests.auth import HTTPBasicAuth


def main():
    test_action = os.getenv('TEST_ACTION')

    if test_action == 'create':
        print('chaos test create ...')

        istio_external_ip = subprocess.os.popen("kubectl get svc -n istio-system | grep ingress | awk '{print$4}'").read().strip()
        print('istio external ip: ', istio_external_ip)
        pulsar_proxy_external_ip = subprocess.os.popen("kubectl get svc -n chaos-" + os.getenv('CLUSTER_ID') + " | grep proxy | awk '{print$4}'").read().strip()
        print('pulsar proxy external ip: ', pulsar_proxy_external_ip)
        subprocess.os.popen("su root")
        for i in range(3):
            subprocess.os.popen("echo '" + istio_external_ip + " chaos-pulsar-" + os.getenv('CLUSTER_ID') + "-broker-" + str(i) + ".pulsar.kop.service' >> /etc/hosts")
        os.system('cat /etc/hosts')

        command = "cd chaos-test && mvn -Dtest=" + os.getenv('TEST_NAME') + " clean test"
        command += " -Dpulsar.deployment.type=EXTERNAL"
        command += " -Dpulsar.external.service.domain=" + pulsar_proxy_external_ip
        command += " -Dchaos.test.duration=" + str(os.getenv('TEST_DURATION'))
        command += " -Dchaos.test.istio.external.ip=" + istio_external_ip
        print('run command: ', command)
        test_res = os.system(command)
        if test_res != 0:
            raise RuntimeError("Chaos test failed code " + test_res + ".")
    elif test_action == 'finish':
        print('chaos test finish ...')

main()
