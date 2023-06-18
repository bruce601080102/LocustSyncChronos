import time, os, configparser
import pandas as pd
from argparse import ArgumentParser
from lib.sample.LocustSysUtils import LocustSysUtils
from lib.sample.SocketUtils import SocketUtils
from hitrustai_lab.log.log_handler import LogHandler
import warnings
warnings.filterwarnings("ignore")

cf = configparser.ConfigParser()
cf.read(os.getcwd() + "/conf/env.conf")
log_handler = LogHandler(service='Locust')
parser = ArgumentParser()
parser.add_argument('-m', default='master', help='選擇模式master/worker/shell')
parser.add_argument('-i', default="127.0.0.1", dest='IP', help='locust master ip')
parser.add_argument('-p', default="5558", dest='Port', help='locust master port')
parser.add_argument('-f', default=None, dest='Pyfile', help='選master後需指定py')
args = parser.parse_args()
mode = args.m
master_host = args.IP
master_port = args.Port
pyfile = args.Pyfile

class LocustSys(LocustSysUtils):
    def __init__(self):
        self.pwd = os.getcwd()
        self.number_users = cf.get("LoadTest", "number_users")
        self.rate = cf.get("LoadTest", "rate")
        self.target_stress_host = cf.get("LoadTest", "target_stress_host")
        self.time_sec = int(cf.get("LoadTest", "time_sec"))
        self.local_host = cf.get("LoadTest", "local_host")

        self.title = cf.get("OutputFile", "title")
        self.savepath = self.pwd + "/" + cf.get("OutputFile", "savepath")

        self.container_name = cf.get("GRPCDockerSet", "container_name")
        self.is_use_docker_set = cf.get("GRPCDockerSet", "is_use_docker_set")
        self.env_cpu_count = cf.get("GRPCDockerSet", "cpu_count")
        self.env_total_ram_gb = int(cf.get("GRPCDockerSet", "total_ram_gb"))

        self.is_open_headless = cf.get("Driver", "is_open_headless")
        self.time_wait = int(cf.get("Driver", "time_wait"))

        # self.conf_master_ip = cf.get("Others", "master_ip")
        self.list_worker_ip = cf.get("Others", "list_worker_ip").split(',')

        self.master_host = master_host
        self.master_port = master_port
        self.status = "0"
        self.cpu_cores = None
        self.ram = None
        self.driver = None
        self.init_logger = log_handler.getlogger('INIT')
        self.socket_utils = SocketUtils(self.init_logger, self.master_host, self.master_port, self.list_worker_ip)

        super().__init__()

    def save_csv(self, list_result, list_time_status):
        request = list_result[1]
        ms1 = list_time_status[5]
        ms2 = list_time_status[7]
        avg_ms = list_result[3]
        rps = list_result[7] 
        fail = int(self.driver.find_element_by_id("fail_ratio").get_attribute("innerHTML"))
        worker_count = self.driver.find_element_by_id("workerCount").text
        dict_result = {
            "類別": self.title,
            "Workers": worker_count,
            "模擬CPU限制": str(self.cpu_cores) + " Cores",
            "模擬RAM限制": str(self.ram) + " GB",
            "模擬客戶數": self.number_users,
            "請求數": request,
            "TPS": rps,
            "90分位數(ms)": ms1,
            "99分位數(ms)": ms2,
            "平均響應時間(ms)": avg_ms,
            "成功率": str(100 - fail) + "%",
            "失敗率": str(fail) + "%"
        }
        try:
            df = pd.read_csv(self.savepath)
        except Exception:
            df = pd.DataFrame()
        df = pd.concat([pd.DataFrame([dict_result]), df]).reset_index(drop=True)
        print("savepath:",self.savepath)
        df.to_csv(self.savepath, encoding='utf_8_sig', index=False)

    def process(self):
        self.begin()
        time.sleep(1)
        if self.is_use_docker_set == "yes":
            self.change_container_format()
        else:
            self.again()

    def run(self):
        if mode == "master":
            self.run_master(pyfile)
            self.socket_utils.client(pyfile)
            # time.sleep(4)
            self.process()
        elif mode == "worker":
            self.socket_utils.run()
        else:
            self.run_shell()
            # time.sleep(10)
            self.process()
            


if __name__ == '__main__':
    ls = LocustSys()
    ls.run()
