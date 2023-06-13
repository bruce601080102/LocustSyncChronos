import streamlit as st
from streamlit.components.v1 import html


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