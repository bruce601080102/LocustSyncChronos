from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--remote-debugging-port=9222")  # 添加此行
options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("http://localhost:8090")
fail = int(driver.find_element_by_id("fail_ratio").get_attribute("innerHTML"))
worker_count = driver.find_element_by_id("workerCount").text

dict_result = {
    "Workers": worker_count,
    "成功率": str(100 - fail) + "%",
    "失敗率": str(fail) + "%"
}
try:
    df = pd.read_csv("output/fraud-detect-predict.csv")
except Exception:
    df = pd.DataFrame()

df = df.append(dict_result, ignore_index=True)
print(df)
df.to_csv("output/fraud-detect-predict.csv", encoding='utf_8_sig', index=False)



# import requests
# from bs4 import BeautifulSoup

# # 发起HTTP请求
# response = requests.get("http://localhost:8090/stats/report")

# # 解析HTML内容
# soup = BeautifulSoup(response.text, "html.parser")

# # 使用类名来查找元素
# elements = soup.find_all(class_="total")

# # 遍历找到的元素
# for element in elements:
#     # 打印元素的文本内容
#     list1 = element.text.split("\n")
#     list1 = [element for element in list1 if element != '']
#     print(list1)
# response.close()
