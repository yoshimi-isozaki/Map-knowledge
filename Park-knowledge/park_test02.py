"""
2021/02/24
14:40
磯嵜佳果
https://www.geocoding.jp/
にて公園名を入力して取得する
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

# geocoding.jpを開く
# 直接小笹３号公園にクエリで入る

#url = 'https://www.geocoding.jp/?q=小笹３号公園%20福岡'33.560544 経度: 130.387521
# 内側の検索機能にアクセスする
url = 'https://www.geocoding.jp/?q=1'
driver.get(url)

time.sleep(3)

keys = '小笹３号公園 福岡'

id = driver.find_element_by_id("searchbox")
id.send_keys(keys)

time.sleep(1)

search_button = driver.find_element_by_xpath("//*[@id='show-map-link']/a")
#search_button.click()
id.send_keys(Keys.ENTER)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

#lat_long = soup.select('#result')
lat_long = soup.find('span', class_="nowrap")

print(lat_long)