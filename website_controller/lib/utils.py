import streamlit as st
from streamlit.components.v1 import html
import subprocess
from subprocess import Popen
from subprocess import PIPE
import re

def hidden_navigation():
    js_code = '''
    $(document).ready(function(){
        $("button[kind=icon]", window.parent.document).remove()
    });
    '''
    # 因为JS不需要展示，所以html宽高均设为0，避免占用空间，且放置在所有组件最后
    # 引用了JQuery v2.2.4
    html(f'''<script src="https://cdn.bootcdn.net/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
        <script>{js_code}</script>''',
        width=0,
        height=0)

    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def kill_os_locust(keyword):
    # keyword = "locust -f"  # 設置 grep 的關鍵字
    ptn = re.compile("\s+")
    p1 = Popen(["ps", "-aux"], stdout=PIPE)
    p2 = Popen(["grep", keyword], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    lines = output.strip().decode().split("\n")
    try:
        for line in lines:
            items = ptn.split(line)
            print("kill {0}...".format(items[1], subprocess.call(["kill", items[1]])))
    except Exception:
        print("第一次啟動")
