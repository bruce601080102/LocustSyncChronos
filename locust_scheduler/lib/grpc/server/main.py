import os
import subprocess
import json


class DocekrCommand:
    def __init__(self):
        self.password = "16313302"
        self.container_name = "abnormal-transaction-predict-pet"

    def execute_docker_update(self):
        command = 'docker update -m 4g --memory-swap -1 --cpus 4 %s' % self.container_name
        _ = os.system('echo %s|sudo -S %s' % (self.password, command))

    def get_docker_cpu(self):
        command = 'docker inspect %s | grep Cpus' % self.container_name
        p = subprocess.getoutput('echo %s|sudo -S %s' % (self.password, command))
        str_result = '{%s}' % p[0:-1]
        cpu_cores = str(json.loads(str_result)["NanoCpus"])[0]
        return cpu_cores

    def get_docker_mem(self):
        command = 'docker inspect %s | grep Mem' % self.container_name
        p = subprocess.getoutput('echo %s|sudo -S %s' % (self.password, command))
        str_result = '{%s}' % p[0:-1]
        print(str_result)
        ram = str(json.loads(str_result)["Memory"])[0]
        return ram


if __name__ == '__main__':
    dc = DocekrCommand()
    ram = dc.get_docker_mem()
    print(ram)


# sudoPassword = '16313302'
# # command = 'docker update -m 4g --memory-swap -1 --cpus 4 diia'
# command = 'docker inspect diia | grep Mem'

# p = subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword, command))
# str_result = '{%s}' % p[0:-1]
# # print(json.loads(str_result)["NanoCpus"])
# print(json.loads(str_result)["Memory"])

# # p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
# # print("------------>",p)
# # str_result = '{%s}' % p
# # print(json.loads(str_result)["NanoCpus"])



