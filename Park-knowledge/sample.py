"""
https://teratail.com/questions/235518
ここから
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import lxml

op = Options()
op.add_argument("--disable-gpu");
op.add_argument("--disable-extensions");
op.add_argument("--proxy-server='direct://'");
op.add_argument("--proxy-bypass-list=*");
op.add_argument("--start-maximized");
# op.add_argument("--headless");
driver = webdriver.Chrome(options=op)

keys = ("ラーメン屋")
url = 'https://www.google.co.jp/maps/'
Selector = 'body'

driver.get(url)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
)

id = driver.find_element_by_id("searchboxinput")
id.send_keys(keys)
time.sleep(2)


Selector = "//*[@id='searchbox-searchbutton']"

search_button = driver.find_element_by_xpath(Selector)
search_button.click()

Selector_login = 'section-result'
WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, Selector_login))
    )
time.sleep(1)

for i in range(len(driver.find_elements_by_class_name(Selector_login))):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, Selector_login))
    )
    login_button = driver.find_elements_by_class_name(Selector_login)[i]
    login_button.click()

    Selector = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/h1'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, Selector))
    )

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    title = soup.find("h1", {"class":"GLOBAL__gm2-headline-5 section-hero-header-title-title"}).text.strip()
    links = soup.find_all(class_="section-info-text")

    print(title, '\n')
    for link in links:
        print(link.text.strip())
    print('---------------------', '\n')

    Selector_back = '//*[@id="pane"]/div/div[1]/div/div/button'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, Selector_back))
    )
    back_button = driver.find_element_by_xpath(Selector_back)
    back_button.click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, Selector_login))
    )