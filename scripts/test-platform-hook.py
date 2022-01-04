#!/usr/bin/env python3

import requests
import sys


class TestPlatformApi:

    _base_url = 'http://127.0.0.1:9091/test-platform/'

    def cluster_start_action(self, cluster_id, action_id):
        url = self._base_url + 'clusters/' + cluster_id + '/start-action/' + action_id
        r = requests.post(url)
        print('cluster link start action: result: ', r)

    def cluster_start_success(self, cluster_id):
        url = self._base_url + 'clusters/' + cluster_id + '/start-success'
        r = requests.post(url)
        print('cluster start success, result: ', r)

    def cluster_start_failed(self, cluster_id):
        url = self._base_url + 'clusters/' + cluster_id + '/start-failed'
        r = requests.post(url)
        print('cluster start failed, result: ', r)

    def cluster_stop_action(self, cluster_id, action_id):
        url = self._base_url + 'clusters/' + cluster_id + '/stop-action/' + action_id
        r = requests.post(url)
        print('cluster link stop action: result: ', r)

    def chaos_exp_link_action(self, exp_id, action_id):
        url = self._base_url + 'chaos-exps/' + exp_id + '/action/' + action_id
        r = requests.post(url)
        print('chaos exp link action. result: ', r)

    def start_finish_chaos_hook(self, exp_id):
        url = self._base_url + 'chaos-exps/' + exp_id + '/finish'
        r = requests.post(url)
        print('start chaos hook: result: ', r)

    def test_link_action(self, test_id, action_id):
        url = self._base_url + 'tests/' + test_id + '/action/' + action_id
        r = requests.post(url)
        print('test link action: result: ', r)

    def test_success(self, test_id):
        url = self._base_url + 'tests/' + test_id + '/success'
        r = requests.post(url)
        print('test is success, result: ', r)

    def test_failed(self, test_id):
        url = self._base_url + 'tests/' + test_id + '/failed'
        r = requests.post(url)
        print('test is failed, result: ', r)


def main():
    if sys.argv.__len__() != 4:
        raise RuntimeError("Miss hook params.")
    action_name = sys.argv[1]
    if action_name is None or action_name == '':
        raise RuntimeError("Miss action name.")
    action_id = sys.argv[2]
    if action_id is None or action_id == '':
        raise RuntimeError("Miss action id.")
    correlation_id = sys.argv[3]
    if id is None or correlation_id == '':
        raise RuntimeError("Miss correlation id.")

    print('test platform hook - action_name: ', action_name, ', action_id: ', action_id, ', correlation_id: ', correlation_id)

    # api = TestPlatformApi()
    # if action_name == 'cluster_start':
    #     api.cluster_start_action(correlation_id, action_id)
    # elif action_name == 'cluster_start_success':
    #     api.cluster_start_success(correlation_id)
    # elif action_name == 'cluster_start_failed':
    #     api.cluster_start_failed(correlation_id)
    # elif action_name == 'cluster_stop':
    #     api.cluster_stop_action(correlation_id, action_id)
    # elif action_name == 'chaos_start':
    #     api.chaos_exp_link_action(correlation_id, action_id)
    # elif action_name == 'chaos_start_finish':
    #     api.start_finish_chaos_hook(correlation_id)
    # elif action_name == 'test_start':
    #     api.test_link_action(correlation_id, action_id)
    # elif action_name == 'test_success':
    #     api.test_success(correlation_id)
    # elif action_name == 'test_failed':
    #     api.test_failed(correlation_id)
    # else:
    #     raise RuntimeError('Unsupported action ' + action_name)


main()
