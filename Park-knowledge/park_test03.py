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
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup

# Google Chromeのドライバを用意
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
wait = WebDriverWait(driver, 10)

# geocoding.jpを開く
# '?q='以下に'%20'で区切って検索語句とする
# url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡市%20西区'
#url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡%20西区'
# 公園名に全角数字が使用されていたら半角にする
table = str.maketrans({'１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9', '０': '0', })
#park_name = '野方８号'
#park_name = '大濠公園'
park_name = 'かなたけの里'
park_name = park_name.translate(table)
print(park_name)
print(type(park_name))
#url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20西区'# 野方８号公園用
url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20中央区' #大濠公園
url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20西区'
driver.get(url)

time.sleep(3)
# "googlemaps"のリンク
gm_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result"]/span[4]/a')))
search_word = driver.find_element_by_xpath('//*[@id="result"]/span[1]')#検索文字列取得
print('検索文字列表示')
print(search_word)
page_source = driver.page_source

# bs4でパース
soup = BeautifulSoup(page_source, 'html.parser')

# spanのうちclass名がnowrapのものを全て
spans = soup.find_all('span', class_='nowrap')
line = None
for elem in spans:
    print(str(elem.text))
    if '緯' in str(elem.text):  # '緯'を含むもの。経緯度の<span>要素だけ欲しい
        line = elem

print('----------------')
print(line.text)  # [緯度: 33.560544 経度: 130.387521]

lat_long = {}  # latが緯度、longが経度
ll_list = []

for val in line.text.split():
    try:
        val = float(val)
    except ValueError:
        val = None
    else:
        ll_list.append(val)

print(list)  # [33.560544, 130.387521]となる
lat_long['緯度'] = ll_list[0]
lat_long['経度'] = ll_list[1]
print(lat_long)

gm_link.click()

"""
url = 'https://www.geocoding.jp/?q=大濠%20公園%20福岡%20中央区'
driver.get(url)
"""

# googlemapの方に切り替える
driver.switch_to.window(driver.window_handles[1])

# 遷移したことを確認するためにurlを取得する
print(driver.current_url)

# !!!!!!!!!!候補がある場合は詳細画面が表示される前!!!!!!!!



# 郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト
list_ad_name = driver.title.split()
print(driver.title.split())
# geocodingの検索文字列とgooglemapの<title>を比べてgooglemap上で検索候補が出たかどうかを知る
search_judge = None # 検索文字列が一致した場合bool型trueが入る
if '福岡' and '西区' in list_ad_name:
    print('合')
    search_judge = True
else:
    print('否')
    search_judge = False
print('search_judge', str(search_judge))




# gm_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result"]/span[4]/a')))
# 候補リストの1番上が出るまで待つ
time.sleep(3)
try:
    first_list = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]')))
except TimeoutException:
    print('もう一つの候補パターン')
    first_list = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]')
first_list.click()


print(driver.title.split())

# 郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト
list_ad_name = driver.title.split()

print(list_ad_name[2])
print(type(list_ad_name[2]))
if list_ad_name[2] == park_name:
    print('合')
elif list_ad_name[2] == park_name + '公園':
    print('合')
elif list_ad_name[2] == park_name + '緑道':
    print('合')
elif list_ad_name[2] == park_name + '緑地':
    print('合')
else:
    print('否')
#例外処理


