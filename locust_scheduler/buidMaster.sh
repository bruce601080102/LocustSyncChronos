#!/bin/bash


locust -f ./scripts/flask_test.py --master --master-bind-port=5558 --web-port=8090 &
locust -f ./scripts/flask_test.py --worker --master-host=localhost --master-port=5558 &