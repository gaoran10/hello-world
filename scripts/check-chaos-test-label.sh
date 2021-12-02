#!/usr/bin/env bash

label = "${LABEL}"

if [ -z $label ]:
  echo 'Miss chaos-test label'
  exit 1
