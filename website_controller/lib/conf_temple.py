conf_temple = """
[LoadTest]
number_users = %s
rate = %s
target_stress_host = %s
time_sec = %s
local_host = %s

[OutputFile]
title = %s
savepath = output/%s

[GRPCDockerSet]
is_use_docker_set = %s
cpu_count = %s
total_ram_gb = %s
container_name = %s

[Driver]
is_open_headless = %s
time_wait = 1

[Others]
master_ip = %s
list_worker_ip = %s
"""







