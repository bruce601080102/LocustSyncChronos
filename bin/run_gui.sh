#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $SCRIPT_DIR
cd $SCRIPT_DIR
cd ..
cd ./website_controller
streamlit run app.py 