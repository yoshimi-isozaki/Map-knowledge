"""
20210212 13:40
yoshimi_isozaki
https://qiita.com/mgmgmogumi/items/f160d28a0643f683afeb#comments
ここのサンプルコードでapiを動かすテストである。
"""

import googlemaps
import pprint # list型やdict型を見やすくprintするライブラリ

key = 'AIzaSyDVTCkHziSZbbVQhDYrb9dvt3zISp5wEMI' # 作成したAPIキーを入れる
client = googlemaps.Client(key) # インスタンス生成

geocode_result = client.geocode('福岡県福岡市香椎駅') # 位置情報を検索
loc = geocode_result[0]['geometry']['location'] # 経度；緯度の情報のみとりだす
place_result = client.places_nearby(location=loc, radius=200, type='restaurant') # 半径200m以内へのレストラン
pprint.pprint(place_result)


