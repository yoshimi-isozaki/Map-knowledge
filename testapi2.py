"""
20210212 16:02
yoshimi_isozaki
https://qiita.com/hmck/items/34b43a1a1d8dd7fd0b5b
ここのサンプルコードでapiを動かすテストである。
ライブラリが足りない
Place ID を調べるなら
https://developers.google.com/places/web-service/place-id
Place Id の場所をgooglemapで表示する構文(id:以下にPlace Idを記す)
https://www.google.com/maps/place/?q=place_id:
'ChIJh6yTsCmSQTUR_VHzKCMdtOk' # 博多もつ鍋専門店(レビュー出ない)
'ChIJX8YWEoeRQTUR3TxhqLNiOr4' # 博多らーめん ちゃんぽん ひるとよる(レビュー出ない)
'ChIJJ4-os2znAGAReJ4AQRGTrcs' # 参考サイトのもの大阪市の御堂筋ホテル(レビュー出る)
'ChIJfxMsDoKRQTURPNe-j5_6unA' # 薬院大通駅（動植物園口）(レビュー出る)
'ChIJNf7wB3-RQTURmeSYqKStQ4E' #マクドナルド 薬院店(レビュー出ない)
'ChIJx-Vi6NaTQTURjNEeOtUgDOM' # 桜坂駅(レビュー出る)
'ChIJI_8Wdo6RQTURMKGLiPmuWu4' # 福岡中央郵便局(レビュー出ない)
'ChIJsye2oAHVQTURnY4wz--Yzoo' # 佐賀県のJR駅相知駅(レビュー出る)
'ChIJiTjyOwbVQTURz6PoJ9ujAbY' # スナックさくら(レビュー出る)
'ChIJuQA_8wjVQTURlGnoJLH8u30' # トーエースポーツ(レビュー出ない,1件だけ)
"""
from bs4 import BeautifulSoup
import requests
#import pprint # list型やdict型を見やすくprintするライブラリ
#import ast # どんなライブラリなのか不明

key = 'AIzaSyDdKdbQVGfN2SgQ2BNEkwAPhK1enpJzk_c' # 上記で作成したAPIキーを入れる
placeId = 'ChIJNf7wB3-RQTURmeSYqKStQ4E' #マクドナルド 薬院店(レビュー出ない)

# 元のコード urlName = "https://maps.googleapis.com/maps/api/place/details/json?placeid={0}&key={1}".format(placeId,key)
urlName = "https://maps.googleapis.com/maps/api/place/details/json?&language=ja&placeid={0}&key={1}".format(placeId,key)

dataHTML = requests.get(urlName)
soup = BeautifulSoup(dataHTML.content, "html.parser")

#soup = ast.literal_eval(str(soup))
#pprint.pprint(soup['result']['reviews'])

ret = soup.find_all('div')
print(soup)
