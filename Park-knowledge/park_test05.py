"""
2021/03/12
10:32
磯嵜佳果
繰り返し処理中に止まった場合何度かやり直す処理を含める
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
# 要素が見つかるまで、最大10秒間待機する
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)  # 10秒待つ。長い

# geocoding.jpを開く
# '?q='以下に'%20'で区切って検索語句とする
# url = 'https://www.geocoding.jp/?q=野方８号%20公園%20福岡%20西区'

# サンプルデータ

sample_dict_list = [{'区': '西区', '種別': '幼児', '公園名': '野方８号', '所在地': '野方六丁目690-113'},
                    {'区': '早良区', '種別': '近隣', '公園名': '田村中央', '所在地': '田村六丁目181-1外'},
                    {'区': '博多区', '種別': '幼児', '公園名': '諸岡２号', '所在地': '諸岡一丁目5-15'},
                    {'区': '博多区', '種別': '幼児', '公園名': '青木１号', '所在地': '青木一丁目217-8'},
                    {'区': '西区', '種別': '街区', '公園名': '元浜', '所在地': '元浜一丁目33-2'},
                    {'区': '西区', '種別': '風致', '公園名': 'かなたけの里', '所在地': '大字金武1282-2外'}
                    ]

sample_dict_list_aft = []  # 後で出来上がった辞書を入れるリスト
# 建艦テーブルを作っている。公園名に全角数字が使用されていたら半角にする

"""
関数digit_zan_han()ないに入る
table = str.maketrans(
    {'１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9', '０': '0', })
"""


# 全角数字を半角数字にするdigit_zen_han()関数を書く
def digit_zen_han(word: str):
    # 建艦テーブルを作っている。公園名に全角数字が使用されていたら半角にする
    table = str.maketrans(
        {'１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9', '０': '0', })
    return word.translate(table)


def latlonger(ward, facility, city):
    facility = digit_zen_han(facility)  # 施設名に全角数字が混じっていた場合に半角にする
    # ↓変数によってgeocodingのurl構成する
    url = 'https://www.geocoding.jp/?q=' + facility + '%20公園%20' + city + '%20' + ward
    driver.get(url)  # seleniumでアクセス
    # 検索結果のページからgooglemapへのリンクを得る
    gm_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result"]/span[4]/a')))
    page_source = driver.page_source  # bs4でパース
    soup = BeautifulSoup(page_source, 'html.parser')

    # spanのうちclass名がnowrapのものを全て
    spans = soup.find_all('span', class_='nowrap')
    line = None
    for elem in spans:
        print(str(elem.text))
        if '緯' in str(elem.text):  # '緯'を含むもの。経緯度の<span>要素だけ欲しい
            line = elem

    print('----------------')
    print('geocodingから取得した文字列', line.text)  # [緯度: 33.560544 経度: 130.387521]

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
    print('geocodingから取得した文字列から辞書にした', lat_long)

    gm_link.click()  # googlemapへ飛ぶ

    # googlemapの方に切り替える
    driver.switch_to.window(driver.window_handles[1])

    # 遷移したことを確認するためにurlを取得する
    print(driver.current_url)

    # 検索フォーム出現まで待つ
    wait.until(EC.element_to_be_clickable((By.ID, "searchbox_form")))
    list_title = driver.title.split()
    print(driver.title.split())

    # !!!!悪魔のコード!!!!
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
    facility_webe = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')))
    print('googlemapから得た施設名facility.text', facility_webe.text)

    if facility_webe.text == facility:
        print('合')
        judg = '合'
    elif facility_webe.text == facility + '公園':
        print('合')
        judg = '合'
    elif facility_webe.text == facility + '緑道':
        print('合')
        judg = '合'
    elif facility_webe.text == facility + '緑地':
        print('合')
        judg = '合'
    else:
        print('否')
        judg = '否'

# ↓返す辞書
    map_info = {}
    print('park_name_gを代入する直前のmap_infoのtypeは', type(map_info))
    park_name_g = facility_webe.text  # googlemapの示す公園名。これを正式名称としたい
    map_info['GM公園名'] = park_name_g
    print('park_name_gのtypeは?', type(park_name_g))
    print("map_info['GM公園名']", map_info['GM公園名'])
    print('typeは?', type(map_info))
    map_info['合否'] = judg
    print("map_info['合否']", map_info['合否'])
    print('typeは?', type(map_info))

    map_info['緯度'] = ll_list[0]
    print("map_info['緯度']", map_info['緯度'])
    print('typeは?', type(map_info))
    map_info['経度'] = ll_list[1]
    print("map_info['経度']", map_info['経度'])
    print('typeは?', type(map_info))
    # ここでappend
    print('最終的にデータベースのレコードとなる構成データ', map_info)
    print('map_infoのtypeは?', type(map_info))
    print('map_info.values()では?', map_info.values())
    print()
    # sample_dict_list_aft.append(map_info)これは返さない

    time.sleep(3)  # closeが早い?
    driver.close()  # googleMapの方を閉じる
    driver.switch_to.window(driver.window_handles[0])  # 動

    return map_info#一行のレコード


# ↑関数終わり
# 新しいfor文。戻り値レコードを
for line in sample_dict_list:
    record = latlonger(line['区'], line['公園名'], '福岡')
    sample_dict_list_aft.append(record)




"""
# !!!これ以下繰り返し
for line in sample_dict_list:

    # サンプルデータからそれぞれ取り出す
    ward = line['区']  # '区'を取り出す
    park_name = line['公園名']  # 公園名を取り出す
    park_name = park_name.translate(table)
    print('サンプルデータから取得し、数字を半角に修正したもの', park_name)
    print()
    url = 'https://www.geocoding.jp/?q=' + park_name + '%20公園%20福岡%20' + ward
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
    print('geocodingから取得した文字列', line.text)  # [緯度: 33.560544 経度: 130.387521]

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
    print('geocodingから取得した文字列から辞書にした', lat_long)

    gm_link.click()  # googlemapへ飛ぶ

    # googlemapの方に切り替える
    driver.switch_to.window(driver.window_handles[1])

    # 遷移したことを確認するためにurlを取得する
    print(driver.current_url)
    # 一例としては郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト
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
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')))
    print('googlemapから得た施設名facility.text', facility.text)

    # //*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]
    # 郵便番号[0]、住所[1]、施設名[2]、'-'[3]、'Googlge'[4]、'マップ'[5]のリスト

    """

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

    map_info = {}
    print('park_name_gを代入する直前のmap_infoのtypeは', type(map_info))
    park_name_g = facility.text  # googlemapの示す公園名。これを正式名称としたい
    map_info['GM公園名'] = park_name_g
    print('park_name_gのtypeは?', type(park_name_g))
    print("map_info['GM公園名']", map_info['GM公園名'])
    print('typeは?', type(map_info))
    map_info['合否'] = judg
    print("map_info['合否']", map_info['合否'])
    print('typeは?', type(map_info))

    map_info['緯度'] = ll_list[0]
    print("map_info['緯度']", map_info['緯度'])
    print('typeは?', type(map_info))
    map_info['経度'] = ll_list[1]
    print("map_info['経度']", map_info['経度'])
    print('typeは?', type(map_info))
    # ここでappend
    print('最終的にデータベースのレコードとなる構成データ', map_info)
    print('map_infoのtypeは?', type(map_info))
    print('map_info.values()では?', map_info.values())
    print()
    sample_dict_list_aft.append(map_info)

    time.sleep(3)  # closeが早い?
    driver.close()  # googleMapの方を閉じる
    driver.switch_to.window(driver.window_handles[0])  # 動かすダブを移動
"""

for line in sample_dict_list_aft:
    print(line)
    print()
