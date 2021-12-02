#!/usr/bin/env bash

body="${COMMENT_BODY}"

res=$(echo $body | grep "== Chaos Cluster Configurations ==")
echo "check res $res"

if [ -z $res ]
then
  echo "Miss chaos cluster configuration header"
  exit 1
else
  echo "Have chaos cluster configuration header"
fi
