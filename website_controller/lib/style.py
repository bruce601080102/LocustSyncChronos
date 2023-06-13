tab = """
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:20px;
}
"""

button = """

#root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: rgb(0 75 75 / 50%);
    font-weight: bold;
    color: white;
}
"""

Style = """
    <style>
        %s

        %s
    </style>
""" % (tab, button) 

