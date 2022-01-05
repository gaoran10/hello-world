#!/usr/bin/env python3

import json
import os
import subprocess
import sys

from chaos_mesh_manually import deploy_exp


def main():
    # if sys.argv.__len__() != 5:
    #     raise RuntimeError("Miss chaos exp params.")
    # exp_type = sys.argv[1]
    # if exp_type is None or exp_type == '':
    #     raise RuntimeError("Miss exp type.")
    # component = sys.argv[2]
    # if component is None or component == '':
    #     raise RuntimeError("Miss exp component.")
    # properties = sys.argv[3]
    # if properties is None or properties == '':
    #     raise RuntimeError("Miss exp properties.")
    # cluster_id = sys.argv[4]
    # if cluster_id is None or cluster_id == '':
    #     raise RuntimeError("Miss exp clusterId.")

    if sys.argv.__len__() != 2:
        raise RuntimeError("Miss chaos exp params.")
    exp_list_json = sys.argv[1]
    if exp_list_json is None or exp_list_json == '':
        raise RuntimeError("Miss exp list json string.")

    exp_list = json.loads(exp_list_json)
    print('Chaos exp deploy ...')
    print(exp_list)
    # exp = {
    #     "expType": exp_type,
    #     "component": component,
    #     "properties": json.loads(properties),
    #     "clusterId": cluster_id
    # }
    # deploy_exp(exp, './hello/chaos-mesh-template')


main()
