#!/bin/bash
arg=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $SCRIPT_DIR
cd $SCRIPT_DIR
cd ..
cd ./locust_scheduler
echo "-->`pwd`"
python=`which python3`
$python main.py -m master -f $arg

