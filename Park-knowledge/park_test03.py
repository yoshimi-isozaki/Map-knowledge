"""
2021/02/25
15:50
磯嵜佳果
https://www.geocoding.jp/
から経緯度を取得してgooglemapに移動して候補があれば
一番上をクリックしてそのページをクリックする。
csvから得られた『公園名』と照合することで確かさを得る。
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
wait = WebDriverWait(driver, 10)

# geocoding.jpを開く
# '?q='以下に'%20'で区切って検索語句とする
url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡市%20西区'
driver.get(url)

time.sleep(3)
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='show-map-link']/a")))
page_source = driver.page_source

#bs4でパース
soup = BeautifulSoup(page_source, 'html.parser')

#spanのうちclass名がnowrapのものを全て
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