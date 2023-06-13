import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import os
from lib.utils import hidden_navigation
from lib.style import Style
from lib.sample import ConfSet, UploadAndSelect
from lib.conf_temple import conf_temple


hidden_navigation()
print(os.getcwd())
pwd = os.getcwd()

# https://blog.csdn.net/weixin_43373042/article/details/123415086
with st.sidebar:
    selected = option_menu("壓測工具", ["Locust", 'Jmeter'], 
        icons=["1 circle", "None"], menu_icon="cast", default_index=0,
        
        styles={
        "container": {"padding": "5!important", "background-color": "transparent !important"},
        # "icon": {"color": "orange", "font-size": "25px"},
        "icon": {"font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
        # "nav-link-selected": {"background-color": "#02ab21"}
        }
        
    )

if selected == "Locust":
    conf_set = ConfSet()
    upload_and_select = UploadAndSelect(pwd)
    tab1, tab2 = st.tabs(["步驟1 設定檔 &nbsp; &nbsp; ▶ ", "步驟2 執行程式"])

    st.markdown(
        Style,
        unsafe_allow_html=True
    )
    print(tab1)

    with tab1:
        conf_set.load_test()
        conf_set.gRPC_docker_set()
        conf_set.web_driver()
        conf_set.output_file()
        conf_set.other()
        _, _, save_col3, _, _ = st.columns(5)
        
        with save_col3:
            save = st.button('儲存')
        if save:
            conf= conf_temple % (
                conf_set.number_users,
                conf_set.rate,
                conf_set.target_stress_host,
                conf_set.time_sec,
                conf_set.local_host,

                conf_set.title,
                conf_set.savepath,

                conf_set.is_use_docker_set,
                conf_set.env_cpu_count,
                conf_set.env_total_ram_gb,
                conf_set.container_name,

                conf_set.driver_option,
                
                conf_set.master_ip,
                conf_set.list_worker_ip,
            )
            with open(pwd + '/conf/env.conf', 'w') as file:
                file.write(conf)
                st.success('The data has been successfully saved!', icon="✅")
            
            with open(pwd.replace("website_controller","locust_scheduler" )+'/conf/env.conf', 'w') as file:
                file.write(conf)
    with tab2:
        upload_and_select.uploader()
        upload_and_select.start_locust()

