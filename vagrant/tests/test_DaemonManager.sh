#!/usr/bin/env bash
set -e

echo "Starting daemon"
python3 ./test_DaemonManager.py start

echo "Sleeping 2"
sleep 2

echo "Testing for pid file."
[ -f "./_.pid" ] || echo "Pid file not found!"

echo "Stopping daemon."
python3 ./test_DaemonManager.py stop

echo "Sleeping 2"
sleep 2

echo "Testing for pid file gone."
[ ! -f "./_.pid" ]  || echo "Pid file not removed!"
