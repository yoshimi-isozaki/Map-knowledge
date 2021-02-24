"""
2021/02/22
11:24
磯嵜佳果
googlemapから公園データを取得するだけのコードを書く #12
selenium_test03.pyを参考にする
htmlのlistを選んで決定する動作が入る
"""

#seleniumとbeautifulsoupをインポート
#import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # どんな作用なのか不明
import time
from bs4 import BeautifulSoup

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
# Google mapsを開く
url = 'https://www.google.co.jp/maps/'
driver.get(url)
wait = WebDriverWait(driver, 20)

time.sleep(3)

#検索欄にキーワードを記入
#keys = input("検索キーワード:") # コマンドライン引数
keys = '福岡市 香椎　公園'

# データ入力
id = driver.find_element_by_id("searchboxinput")#googlemapの検索ボックスのidを指定して要素を取得している
id.send_keys(keys) #

time.sleep(1)

#クリック
search_button = driver.find_element_by_xpath("//*[@id='searchbox-searchbutton']") #xpathで要素を取得している
search_button.click() # クリックしている

time.sleep(3)

#login_button = driver.find_element_by_class_name("section-result-title") # ログインボタンを取得
login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-title")))
login_button.click() # クリックしている

time.sleep(3)
#//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]
list_one = None
try:
    list_one = wait.until(EC.element_to_be_clickable((By.XPATH, "*[@id='pane']/div/div[1]/div/div/div[4]/div[1]/div[1]")))
except TimeoutException:
    print('タイムアウト')
else:
    list_one.click()
#/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div[1]
# xpass削る//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]
#1//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]
#2//*[@id="pane"]/div/div[1]/div/div/div[4]
#elements = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div[1]")
#elements = driver.find_element_by_class_name("section-result")_css_selector(".a-link-sample.a-text-normal")
#elements = driver.find_element_by_css_selector(".section-result")
#print(elements)
#targetelement = None
# for(element in elements) 名前が似ているなどの条件を付加してここで精査する
#targetelement = elements[0]要素数で指定したいができない
#elements.click()

# HTMLを解析
page_source = driver.page_source # pagesource取得。これはseleniumのインスタンス
soup = BeautifulSoup(page_source, 'html.parser') #seleniumのインスタンスがbsによってパースされる

# 取得したい要素を取得
title = soup.find(class_="GLOBAL__gm2-headline-5 section-hero-header-title-title")
link = soup.find_all(class_="section-info-text")

# 現在のurlを取得
cur_url = driver.current_url

# 出力
print("------------------------------------")
print(cur_url)
print(soup.title)
print(soup.title.string)
print(len(soup.title.string))
#print(soup.find_all('span'))
# .get_text(strip=True)
#print(soup.text)
#print(title.text.strip())
#print(link[0].text.strip())
#print(link[2].text.strip())
#print(link[3].text.strip())
print("------------------------------------")