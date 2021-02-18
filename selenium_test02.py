"""
2021/02/18/14:11磯嵜佳果
seleniumのテスト02
https://qiita.com/mastar_3104/items/0a1ce2bfa1d29287bc35
"Google検索するSeleniumを実装"
検索ボタンを押してもらうことができなかった
https://watlab-blog.com/2019/08/11/selenium-google-search/
こちらを参考にして改造
timeをimportしsearch()を使用した
"""
import time
from selenium import webdriver #SeleniumWebdriverをインポートして

driver = webdriver.Chrome("/usr/local/bin/chromedriver") #Chromeを動かすドライバーを読み込み

driver.get("https://google.co.jp")

time.sleep(2)
text = driver.find_element_by_name("q")# ID属性から検索用テキストボックスの要素を取得し
text.send_keys("selenium") # 文字列"selenium"をテキストボックスに入力

#btn = driver.find_element_by_name("btnK") # 検索用ボタンにはID属性がないのでname属性から取得し
#btn.click() # 対象をクリック!

time.sleep(3)
text.submit()
time.sleep(5)
driver.quit()