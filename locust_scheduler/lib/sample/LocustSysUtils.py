import time
import re
import requests
import subprocess
import requests
import socket
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import Popen
from subprocess import PIPE
from threading import Timer
from lib.grpc.client import connect_grpc_execute_update, connect_grpc
import logging

# 设置日志级别为ERROR或更高级别
logging.getLogger('locust').setLevel(logging.ERROR)


class ConnectionRPC:
    def change_container_format(self):
        for _, cpu in enumerate(self.cpu_list):
            print("----->", cpu)
            cpu_ram = "%s,%s,%s" % (cpu, self.env_total_ram_gb, self.container_name)
            connect_grpc_execute_update(cpu_ram)
            time.sleep(self.time_wait)
            result = connect_grpc(cpu_ram)
            print("環境設定:%s - docker回傳設定:%s" % (cpu_ram, result))
            r = result.split(",")
            self.cpu_cores = r[0]
            self.ram = r[1]
            self.again()
            time.sleep(self.time_sec + 5)


class LocusAction:
    def webdriver_set(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--remote-debugging-port=9222")  # 添加此行

        if self.is_open_headless == "yes":
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.local_host)

    def connection_report(self):
        response = requests.get(self.local_host + "/stats/report")
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(class_="total")
        response.close()

        list_result = elements[0].text.split("\n")
        list_result = [element for element in list_result if element != '']

        list_result1 = elements[1].text.split("\n")
        list_result1 = [element for element in list_result1 if element != '']       
        return list_result, list_result1

    def stop(self):
        self.init_logger.info("========= 4 start=========")
        requests.get(self.local_host + '/stop')
        time.sleep(5)
        if self.status == "1":
            list_result, list_time_status = self.connection_report()
            time.sleep(3) # 等待
            self.save_csv(list_result, list_time_status)
            self.driver.close()
            self.init_logger.info("已將結果存入csv")
        self.init_logger.info("========= 4 end=========")
        with open(self.pwd + "/log/output.txt", "a") as file:
            file.writelines("end")

    def begin(self):
        self.status = "0"
        # self.locust_time()
        self.webdriver_set()
        self.init_logger.info("========= 3 start=========")
        self.init_logger.info("開始操作locust頁面")
        try:
            
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[1]").send_keys(self.number_users)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[2]").send_keys(self.rate)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[3]").send_keys(self.target_stress_host)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/button").click()
            self.init_logger.info("第一次操作頁面")
        except Exception:
            self.init_logger.info("不是第一次操作頁面")

        time.sleep(1)
        self.init_logger.info("========= 3 end=========")
        self.stop()

    def again(self):
        self.status = "1"
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/a[1]").click()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[1]").clear()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[1]").send_keys(self.number_users)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[2]").clear()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[2]").send_keys(self.rate)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[3]").clear()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/input[3]").send_keys(self.target_stress_host)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/form/button").click()
        except Exception as e:
            print(e)
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/a[2]").click()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/input[1]").clear()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/input[1]").send_keys(self.number_users)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/input[2]").clear()
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/input[2]").send_keys(self.rate)
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/button").click()
        self.init_logger.info("locust頁面中點擊開始")
        # 打开文件并写入内容
        with open(self.pwd + "/log/output.txt", "w") as file:
            file.writelines("dirver start\n")

        t = Timer(self.time_sec, self.stop)
        t.start()


class LocustWebServer:
    def run_shell_script(self):
        self.init_logger.info("========= 2 start=========")
        time.sleep(2)
        subprocess.Popen(args='./buidMaster.sh', shell=False)
        self.init_logger.info("啟動shell script")
        self.init_logger.info("========= 2 end=========")
        
        # subprocess.Popen(args='locust -f ./scripts/{} --master --master-bind-port=5558 --web-port=8090'.format(self.locals_file), shell=True)
        # print("master")
        # subprocess.Popen(args='locust -f ./scripts/{} --worker --master-host=192.168.10.109 --master-port=5558'.format(self.locals_file), shell=True)
        # print("workers")
        # try:
        #     workers = self.workers.split(",")
        #     workers.remove("")
        # except Exception:
        #     pass
        # for worker in workers:
        #     worker = worker.split(":")
        #     worker_ip = worker[0]
        #     worker_port = worker[1]
        #     # print("{}:{}".format(worker_ip, worker_port))
        #     subprocess.Popen(args="ssh -p {} root@{} 'locust -f /root/stress-test/scripts/{} --worker --master-host=192.168.10.109 --master-port=5558'".format(worker_port, worker_ip, self.locals_file), shell=True)
        #     os.system("sshpass -p 16313302 ssh -p {} -o StrictHostKeyChecking=no -i {} root@{} 'locust -f {} --worker --master-host=192.168.10.109 --master-port=5558'".format(worker_port, self.identity_file, worker_ip, self.locals_file))

    def listen_port(self, host, port):
        try:
            # 建立TCP socket對象
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 設置超時時間為1秒
            sock.settimeout(1)
            
            # 嘗試連接到目標主機和端口
            result = sock.connect_ex((host, port))
            # 關閉socket連接
            sock.close()
            # 根據連接結果進行判斷
            if result == 0:
                # print(f"Port {port} is open")
                return 1
            else:
                # print(f"Port {port} is closed")
                return 0
        except socket.error as e:
            print(f"Error: {e}")

    def kill_os_locust(self, keyword):
        # keyword = "locust -f"  # 設置 grep 的關鍵字
        ptn = re.compile("\s+")
        p1 = Popen(["ps", "-aux"], stdout=PIPE)
        p2 = Popen(["grep", keyword], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        output = p2.communicate()[0]
        lines = output.strip().decode().split("\n")
        self.init_logger.info("========= 1 start=========")
        try:
            for line in lines:
                items = ptn.split(line)
                self.init_logger.info("kill {0}...".format(items[1], subprocess.call(["kill", items[1]])))
        except Exception:
            self.init_logger.info("第一次啟動")
        self.init_logger.info("========= 1 end=========")

    def run_master(self, locals_file):
        gui_port = int(self.local_host.split(":")[-1])
        self.kill_os_locust(keyword="master-bind-port=5558")
        while True:
            res = self.listen_port("127.0.0.1", 5558)
            if res == 0:
                break
        subprocess.Popen(args='locust -f {}/scripts/{} --master --master-bind-port=5558 --web-port={}'.format(self.pwd, locals_file, gui_port), shell=True)

    def run_worker(self, locals_file):
        print('locust -f {}/scripts/{} --worker --master-host={} --master-port={}'.format(self.pwd, locals_file, self.master_host, self.master_port))
        self.kill_os_locust(keyword="master-port=%s" % (self.master_port))
        subprocess.Popen(args='locust -f {}/scripts/{} --worker --master-host={} --master-port={}'.format(self.pwd, locals_file, self.master_host, self.master_port), shell=True)
    
    def run_shell(self):
        self.kill_os_locust("locust -f") 
        time.sleep(5) 
        self.run_shell_script()

class LocustSysUtils(ConnectionRPC, LocusAction, LocustWebServer):
    def __init__(self):
        self.cpu_list = self.env_cpu_count.split(",")
