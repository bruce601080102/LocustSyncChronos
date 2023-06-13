import os
import subprocess
import json


class DocekrCommand:
    def __init__(self):
        self.password = "16313302"
        self.container_name = "abnormal-transaction-predict-pet"
        self.cores = None
        self.ram = None

    def execute_docker_update(self):
        command = 'docker update -m %sg --memory-swap -1 --cpus %s %s' % (self.ram, self.cores, self.container_name)
        print(command)
        _ = os.system('echo %s|sudo -S %s' % (self.password, command))

    def get_docker_cpu(self):
        
        command = 'docker inspect %s | grep Cpus' % self.container_name
        p = subprocess.getoutput('echo %s|sudo -S %s' % (self.password, command))
        str_result = '{%s}' % p[0:-1]
        str_cpu_cores = str(json.loads(str_result)["NanoCpus"])
        cpu_cores = str(int(str_cpu_cores) // 1000000000)
        return cpu_cores

    def get_docker_mem(self):
        command = 'docker inspect %s | grep Mem' % self.container_name
        p = subprocess.getoutput('echo %s|sudo -S %s' % (self.password, command))
        str_result = '{%s}' % p[0:-1]
        str_ram = str(json.loads(str_result)["Memory"])
        ram = str(int(str_ram) // (1024**3))
        return ram


# 這是查詢現在的狀態
def dockerinfo(name):
    cr = name.split(",")
    dc = DocekrCommand()
    dc.container_name = cr[2]
    ram = dc.get_docker_mem()
    cpu_cores = dc.get_docker_cpu()
    return f"{cpu_cores},{ram}"


# 更新容器的狀態
def executeupdate(name):
    cr = name.split(",")
    dc = DocekrCommand()
    dc.cores = cr[0]
    dc.ram = cr[1]
    dc.container_name = cr[2]
    dc.execute_docker_update()
    return f"==已更換==="
