"""
2021/02/18/14:11磯嵜佳果
seleniumのテスト
https://qiita.com/mastar_3104/items/0a1ce2bfa1d29287bc35
"たった三行のコード"
"""
from selenium import webdriver #SeleniumWebdriverをインポートして

driver = webdriver.Chrome("/usr/local/bin/chromedriver") #Chromeを動かすドライバーを読み込み

driver.get("https://google.co.jp")