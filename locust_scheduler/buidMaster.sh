#!/bin/bash


locust -f ./scripts/flask_test.py --master --master-bind-port=5558 --web-port=8090 &
locust -f ./scripts/flask_test.py --worker --master-host=localhost --master-port=5558 &


# locust -f locust_test.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f locust_test.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f locust_test.py --worker --master-host=localhost --master-port=5557 &

# locust -f ./scripts/card_test.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/card_test.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/card_test.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/card_test.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/abnormal_transaction_v1.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/abnormal_transaction_v1.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/abnormal_transaction_v1.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/abnormal_transaction_v1.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/abnormal_transaction_v2.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/abnormal_transaction_v2.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/abnormal_transaction_v2.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/abnormal_transaction_v2.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/fraud_detect_v1.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/fraud_detect_v1.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/fraud_detect_v1.py --worker --master-host=localhost --master-port=5557 &

# locust -f ./scripts/fraud_detect_v2_r1.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/fraud_detect_v2_r1.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/fraud_detect_v2_r1.py --worker --master-host=localhost --master-port=5557 &

# locust -f ./scripts/fraud_detect_v2_r2.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/fraud_detect_v2_r2.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/fraud_detect_v2_r2.py --worker --master-host=localhost --master-port=5557 &

# locust -f ./scripts/fraud_detect_v3_r1.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/fraud_detect_v3_r1.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/fraud_detect_v3_r1.py --worker --master-host=localhost --master-port=5557 &

# locust -f ./scripts/fraud_detect_v3_r2.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/fraud_detect_v3_r2.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/fraud_detect_v3_r2.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/fraud_detect_v3_r2.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/diia_get_v3_js.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/diia_get_v3_js.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/diia_get_v3_js.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/diia_get_v3_js.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/diia_get_v4_js.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/diia_get_v4_js.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/diia_get_v4_js.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/diia_get_v4_js.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/diia_post_saveinfo.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/diia_post_saveinfo.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/diia_post_saveinfo.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/diia_post_saveinfo.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/rule_engine.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/rule_engine.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/rule_engine.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/rule_engine.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/rule_engine_server.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/rule_engine_server.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/rule_engine_server.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/rule_engine_server.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/acs_auth.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/acs_auth.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/acs_auth.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/acs_auth.py --worker --master-host=192.168.10.109 --master-port=5558 &

# locust -f ./scripts/updateData.py --master --master-bind-port=5557 --web-port=8089 &
# locust -f ./scripts/updateData.py --master --master-bind-port=5558 --web-port=8090 &
# locust -f ./scripts/updateData.py --worker --master-host=localhost --master-port=5557 &
# locust -f ./scripts/updateData.py --worker --master-host=192.168.10.109 --master-port=5558 &
