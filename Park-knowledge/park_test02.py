"""
2021/02/24
14:40
磯嵜佳果
https://www.geocoding.jp/
にて公園名を入力して取得する
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time
from bs4 import BeautifulSoup

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
wait = WebDriverWait(driver, 10)
# geocoding.jpを開く
# 直接小笹３号公園にクエリで入る

#url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡'33.560544 経度: 130.387521
# 内側の検索機能にアクセスする
url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡市%20西区'
driver.get(url)

time.sleep(3)
"""
keys = '小笹３号公園 福岡'

id = driver.find_element_by_id("searchbox")
id.send_keys(keys) # 検索ボックスに検索キーワードを入力
"""
time.sleep(1)

# list_one = wait.until(EC.element_to_be_clickable((By.XPATH, "*[@id='pane']/div/div[1]/div/div/div[4]/div[1]/div[1]")))
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='show-map-link']/a")))
#search_button.click()
#id.send_keys(Keys.ENTER)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

#lat_long = soup.select('#result')
#lat_long = soup.find('span', class_="nowrap")
spans = soup.find_all('span', class_ ='nowrap')
line = None
for elem in spans:
    print(str(elem.text))
    if '緯' in str(elem.text):# '緯'を含むもの。経緯度の<span>要素だけ欲しい
        line = elem

print('----------------')
print(line.text)# [緯度: 33.560544 経度: 130.387521]

lat_long = {} # latが緯度、longが経度
list = []


for val in line.text.split():
    try:
        val = float(val)
    except ValueError:
        val = None
    else:
        list.append(val)

print(list) #[33.560544, 130.387521]となる
lat_long['緯度'] = list[0]
lat_long['経度'] = list[1]
print(lat_long)