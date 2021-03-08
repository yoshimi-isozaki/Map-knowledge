"""
2021/03/01
10:50
磯嵜佳果
geocodingから情報を得るコード
サンプルの情報をfor文で回す
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
wait = WebDriverWait(driver, 11)  # 10秒待つ。長い

# geocoding.jpを開く
# '?q='以下に'%20'で区切って検索語句とする
# url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡市%20西区'
# url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡%20西区'

# サンプルデータ

sample_dict_list = [{'区': '西区', '種別': '幼児', '公園名': '野方８号', '所在地': '野方六丁目690-113'},
                    {'区': '早良区', '種別': '近隣', '公園名': '田村中央', '所在地': '田村六丁目181-1外'},
                    {'区': '博多区', '種別': '幼児', '公園名': '諸岡２号', '所在地': '諸岡一丁目5-15'},
                    {'区': '博多区', '種別': '幼児', '公園名': '青木１号', '所在地': '青木一丁目217-8'},
                    {'区': '西区', '種別': '街区', '公園名': '元浜', '所在地': '元浜一丁目33-2'},
                    {'区': '西区', '種別': '風致', '公園名': 'かなたけの里', '所在地': '大字金武1282-2外'}
                    ]

sample_dict_list_aft = [] # 後で出来上がった辞書を入れるリスト
# 公園名に全角数字が使用されていたら半角にする
table = str.maketrans(
    {'１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9', '０': '0', })
#!!!これ以下繰り返し
for line in sample_dict_list:

    # park_name = '野方８号'
    # park_name = '大濠公園'
    # サンプルデータからそれぞれ取り出す
    #ward = list(sample_dict_list[1].values())[0]  # '区'を取り出す
    ward = line['区']
    #park_name = list(sample_dict_list[1].values())[2]  # 公園名を取り出す
    park_name = line['公園名']
    park_name = park_name.translate(table)
    print(park_name)
    # url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20西区'# 野方８号公園用
    # url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20中央区' #大濠公園
    url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20' + ward  # 田村中央公園
    driver.get(url)

    time.sleep(3)
    # "googlemaps"のリンク
    gm_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result"]/span[4]/a')))
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

    gm_link.click()  # googlemapへ飛ぶ

    # googlemapの方に切り替える
    driver.switch_to.window(driver.window_handles[1])

    # 遷移したことを確認するためにurlを取得する
    print(driver.current_url)
    # 郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト
    # 検索フォーム出現まで待つ
    wait.until(EC.element_to_be_clickable((By.ID, "searchbox_form")))
    list_title = driver.title.split()
    print(driver.title.split())
    # 候補リストの1番上が出るまで待つ

    search_judge = None  # 検索文字列が一致した場合bool型trueが入る
    if '福岡' and ward in list_title:
        print('合:候補がある場合')
        search_judge = True
        # 候補の一番上を選びクリックする
        first_list = None
        try:
            first_list = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]')))
        except TimeoutException:
            print('もう一つの候補パターン')
            first_list = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]')
        first_list.click()
    else:
        print('否:すぐに詳細画面が表示される')
        search_judge = False
    print('search_judge', str(search_judge))

    print(driver.title.split())
    # 施設名のspan//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]
    facility = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')))
    print(facility.text)

    # //*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]
    # 郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト


    """
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
    """

    # 'facility.text'は施設名,変数
    print('facility.text')
    print(type(facility.text))

    if facility.text == park_name:
        print('合')
        judg = '合'
    elif facility.text == park_name + '公園':
        print('合')
        judg = '合'
    elif facility.text == park_name + '緑道':
        print('合')
        judg = '合'
    elif facility.text == park_name + '緑地':
        print('合')
        judg = '合'
    else:
        print('否')
        judg = '否'

    park_name_g = facility.text # googlemapの示す公園名。これを正式名称としたい。
    line['GM公園名'] = park_name_g
    line['合否'] = judg

    line['緯度'] = ll_list[0]
    line['経度'] = ll_list[1]
    # ここでappend
    print('構成データ', line)
    print()
    sample_dict_list_aft.append(line)

    time.sleep(3)# closeが早い?
    driver.close() # googleMapの方を閉じる
    driver.switch_to.window(driver.window_handles[0]) # 動かすダブを移動

for line in sample_dict_list_aft:
    print(line)
    print()
