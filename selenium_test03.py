"""
2021/02/18/14:59磯嵜佳果
seleniumのテスト03
https://su-gi-rx.com/archives/3217
seleniumを使ってgooglemapからスクレイピングするトレーニング
取得する情報はなんでもいい
"""

#seleniumとbeautifulsoupをインポート
#import chromedriver_binary
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import bs4

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
# Google mapsを開く
url = 'https://www.google.co.jp/maps/'
driver.get(url)

time.sleep(5)

#検索欄にキーワードを記入
keys = input("検索キーワード:") # 入力する

# データ入力
id = driver.find_element_by_id("searchboxinput")
id.send_keys(keys)

time.sleep(1)

#クリック
search_button = driver.find_element_by_xpath("//*[@id='searchbox-searchbutton']")
search_button.click()

time.sleep(3)

login_button = driver.find_element_by_class_name("section-result-title")
login_button.click()

time.sleep(3)

# HTMLを解析
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 取得したい要素を取得
title = soup.find(class_="GLOBAL__gm2-headline-5 section-hero-header-title-title")
link = soup.find_all(class_="section-info-text")

# 現在のurlを取得
cur_url = driver.current_url

# 出力
print("------------------------------------")
print(cur_url)
print(soup.title)
print(soup.find('h1'))
#print(soup.find_all('span'))
# .get_text(strip=True)
#print(soup.text)
#print(title.text.strip())
#print(link[0].text.strip())
#print(link[2].text.strip())
#print(link[3].text.strip())
print("------------------------------------")