#!/usr/bin/env python3

import requests
import sys

class TestPlatformApi:

    _base_url = 'http://103.149.181.34:8080/test-platform/chaos-exps/'

    def start_chaos_hook(self, exp_id):
        url = self._base_url + 'start/' + exp_id + '/hook'
        print('url: ', url)
        r = requests.post(url)
        print('start chaos hook: result: ', r)

    def start_finish_chaos_hook(self, exp_id):
        url = self._base_url + 'start-finish/' + exp_id + '/hook'
        r = requests.post(url)
        print('start chaos hook: result: ', r)


def main():
    if sys.argv.__len__() != 3:
        raise RuntimeError("Miss hook params.")
    action_name = sys.argv[1]
    if action_name is None or action_name == '':
        raise RuntimeError("Miss action name.")
    id = sys.argv[2]
    if id is None or id == '':
        raise RuntimeError("Miss correlation id.")

    api = TestPlatformApi()
    if action_name == 'start_chaos':
        api.start_chaos_hook(id)
    elif action_name == 'start_finish_chaos':
        api.start_finish_chaos_hook(id)
    else:
        raise RuntimeError('Unsupported action ' + action_name)

main()
