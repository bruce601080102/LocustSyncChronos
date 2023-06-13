import streamlit as st
import configparser
import time
import pandas as pd
from stqdm import stqdm
import streamlit.components.v1 as components
import subprocess
import pandas as pd

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

cf = configparser.ConfigParser()

class ConfSet:
    def __init__(self):
        cf.read("./conf/env.conf")
        self.number_users = int(cf.get("LoadTest", "number_users"))
        self.rate = int(cf.get("LoadTest", "rate"))
        self.target_stress_host = cf.get("LoadTest", "target_stress_host")
        self.time_sec = int(cf.get("LoadTest", "time_sec"))
        self.local_host = cf.get("LoadTest", "local_host")

        self.title = cf.get("OutputFile", "title")
        self.savepath = cf.get("OutputFile", "savepath")
        
        self.is_use_docker_set = cf.get("GRPCDockerSet", "is_use_docker_set")
        self.env_cpu_count = cf.get("GRPCDockerSet", "cpu_count")
        self.env_total_ram_gb = int(cf.get("GRPCDockerSet", "total_ram_gb"))
        self.container_name = cf.get("GRPCDockerSet", "container_name")
        self.is_open_headless = cf.get("Driver", "is_open_headless")
        
        self.master_ip = cf.get("Others", "master_ip")
        self.list_worker_ip = cf.get("Others", "list_worker_ip")
        self.count = 0

    def load_test(self):
        st.subheader('【Locust設定】')
        col1, col2 = st.columns(2)
        with col1:
            self.number_users = st.number_input(label='設定需要同時打入幾個請求', value=self.number_users, max_value=999999, min_value=0,step=1)
            self.rate = st.number_input(label='每一秒提升多少請求', value=self.rate, max_value=999999, min_value=0,step=1)
        with col2:
            self.target_stress_host = st.text_input('需要壓測的網址', self.target_stress_host)
            self.time_sec = st.number_input(label='需要壓測多少秒', value=self.time_sec, max_value=999999, min_value=0,step=1)
        self.local_host = st.text_input('爬蟲程式需要訪到哪一個locust的頁面中', self.local_host)
        
    def gRPC_docker_set(self):
        st.subheader('【gRPC Docker Set】')
        if self.is_use_docker_set == "yes":
            index=1
        else:
            index=0
        option = st.selectbox(
            '是否需要使用grpc連線並設定docker規格',
            ('no', 'yes'),
            index=index
        )
        if option == "yes":
            grpc_col1, grpc_col2, grpc_col3 = st.columns(3)
            with grpc_col1:
                self.env_cpu_count = st.text_input('需要更改的核心數', self.env_cpu_count)
            with grpc_col2:
                self.env_total_ram_gb = st.number_input('需要更改的ram',  value=self.env_total_ram_gb, max_value=256, min_value=1,step=1)
            with grpc_col3:
                self.container_name = st.text_input('需要改變的container名稱', self.container_name)
    
    def web_driver(self):
        if self.is_open_headless == "yes":
            index=1
        else:
            index=0
        st.subheader('【爬蟲程式設定】')
        self.driver_option = st.selectbox(
            '是否啟動無痕模式',
            ('no', 'yes'), 
            index=index
        )

    def output_file(self):
        st.subheader('【Output File】')
        output_file_col1, output_file_col2 = st.columns(2)
        with output_file_col1:
            self.title = st.text_input('給此次任務一個名稱', self.title)
        with output_file_col2:
            path = self.savepath.split("output/")[1]
            self.savepath = st.text_input('存入路徑的檔案(csv)',  path)

    def other(self):
        st.subheader('【其它設定】')
        other_file_col1, other_file_col2 = st.columns(2)
        
        worker_ip = self.list_worker_ip.split(",")
        
        with other_file_col1:
            self.master_ip = st.text_input('master節點的內網', self.master_ip)
        with other_file_col2:
            self.worker_number = st.number_input(label='有幾個worker節點', value=len(worker_ip), max_value=999999, min_value=0,step=1)
        
        list_worker = []
        if self.worker_number > 0:
            for index in range(self.worker_number): 
                try:
                    conf_ip = worker_ip[index]
                except Exception:
                    conf_ip = ""
                value = st.text_input(f"輸入Worker IP", conf_ip, key=index)
                if value != "":
                    list_worker.append(value)
        self.list_worker_ip = ",".join(list_worker)


class UploadAndSelect:
    def __init__(self, pwd):
        self.time_sec = int(cf.get("LoadTest", "time_sec"))
        self.local_host = cf.get("LoadTest", "local_host")
        self.savepath = cf.get("OutputFile", "savepath")
        self.pwd = pwd
        self.target_file = None

    def uploader(self):
        uploaded_files = st.file_uploader("Choose a locust *.py file")
        
        if uploaded_files is not None:
            try:
                py = uploaded_files.read().decode('utf-8')
                pwd = self.pwd.replace("website_controller","locust_scheduler" )
                self.target_file = uploaded_files.name
                with open(pwd + "/scripts/" + uploaded_files.name, "w", encoding="utf-8") as file:
                    file.write(py)
            except Exception as e:
                print(e)
                st.error("請上傳.py")

    def start_locust(self):
        _, _, start_col3, _, _ = st.columns(5)
        
        with start_col3:
            start = st.button('執行壓測')
        if start:
            import os
            if self.target_file is not None:
                # subprocess.Popen(args=["../bin/run_locust.sh" ,self.target_file])
                subprocess.Popen(args=["../bin/run_locust.sh" ,self.target_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with start_col3:
                    with st.spinner('Preparing the WebDriver. Please wait a moment.'):
                        while True:
                            with open("../locust_scheduler/log/output.txt", "r") as file:
                                content = file.read()
                                if "dirver start" in content:
                                    break
                for _ in stqdm(range(self.time_sec)):
                    time.sleep(1)

                with start_col3:
                    with st.spinner('The CSV file is being saved. Please wait a moment.'):
                        while True:
                            with open("../locust_scheduler/log/output.txt", "r") as file:
                                content = file.read()
                                if "end" in content:
                                    break
                st.success('Done!')
                df = pd.read_csv("../locust_scheduler/output/fraud-detect-predict.csv")
                self.download_csv()
                st.dataframe(df.head())
                with open("../locust_scheduler/log/output.txt", "w") as file:
                    file.truncate(0)
            else:
                st.error("請上傳.py")

        # iframe_html = '''
        # <div style="position: relative; padding-bottom: 90.25%;padding-right: 100%; height: 0;">
        #     <iframe src="http://localhost:8090/" frameborder="0" allowfullscreen
        #         style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
        # </div>
        # '''
        # st.markdown(iframe_html, unsafe_allow_html=True)

    def download_csv(self):
        pwd = self.pwd.replace("website_controller","locust_scheduler" )
        df = pd.read_csv(pwd + f"/{self.savepath}")
        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=self.savepath,
            mime='text/csv',
        )