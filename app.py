import time

import requests
import streamlit as st
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

st.title("三菱UFJ銀行為替情報アプリ")

URL_1 = 'http://www.murc-kawasesouba.jp/fx/index.php'
URL_2 = 'https://www.bk.mufg.jp/ippan/rate/real.html'


# HTMLの対象とする画像のパス：XPath 検証ツールからコピー可能
RATE_IMG = '//*[@id="main"]/div[3]/p[2]/img'
# TTS(日本円→外貨)
USD_TTS_PATH = '/html/body/div[1]/div/div/div[2]/main/article/div/div[1]/div/table/tbody/tr[1]/td[1]'
# TTB(外貨→日本円)
USD_TTB_PATH = '/html/body/div[1]/div/div/div[2]/main/article/div/div[1]/div/table/tbody/tr[1]/td[2]'

UPDATE_PATH = '/html/body/div[1]/div/div/div[2]/main/article/div/div[1]/div/div[2]/div[2]/p/span'
# spread
spread = 0


driver_path = ChromeDriverManager().install()
#ブラウザを開く描写をしない
options = Options()
options.add_argument('--headless')  
options.add_argument('--disable-web-security')
#options=chrome_options
# ブラウザをChromeに設定
driver_1 = webdriver.Chrome(service=Service(executable_path=driver_path),options=options)
driver_2 = webdriver.Chrome(service=Service(executable_path=driver_path),options=options)
# getrequest
driver_1.get(URL_1)
time.sleep(3)
driver_2.get(URL_2)
time.sleep(3)
img_element = WebDriverWait(driver_1, 10).until(lambda x: x.find_element(By.XPATH, RATE_IMG))
tts_element = WebDriverWait(driver_2, 10).until(lambda x: x.find_element(By.XPATH, USD_TTS_PATH))
ttb_element = WebDriverWait(driver_2, 10).until(lambda x: x.find_element(By.XPATH, USD_TTB_PATH))
update_datetime = WebDriverWait(driver_2, 10).until(lambda x: x.find_element(By.XPATH, UPDATE_PATH))



# Web上の画像URLを取得
img_url = img_element.get_attribute("src")
print(img_url)

# 画像要素取得
img_content = requests.get(img_url).content

with open("kawase.png", "wb") as w:
        w.write(img_content)

image = Image.open("kawase.png")
st.image(image)
        

driver_1.quit()
driver_2.quit()
