import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import def_

# selenium 최신버전 문법이 바뀌어서 기존의 문법으로 이용하려면 selenium 3.14.1 버전 설치
# pip install selenium==3.14.1

# 이번엔 최신 버전의 selenium 문법 이용
# pip install selenium

"------------------------------------------------------------------------------------------"

## 일정 정리
    ## 런던의 경우 9박 10일 일정을 계획 ## 
    ## 가는 날 리스트만들기 (22년 9월 28일부터 23년 8월월 31일까지)##

# 출발 일자 리스트 정리 
day_depart = def_.day_month[27:] # 9월 28일부터 8월 31일까지 day만 나열되어있는 리스트 생성

idx_ls = def_.what_idx_ls()
idx_ls_depart = idx_ls[27:] # 9월 28일부터 중복되는 몇번째 값인지 나열되어있는 리스트 생성

# 도착 일자 리스트 정리
day_back = def_day_month[36:]
idx_ls_back = idx_ls[36:]

def scrape_london():
    browser = webdriver.Chrome("/Users/ijeong-an/Desktop/codestates/cp2/chromedriver.exe")
    browser.maximize_window() # 창 최대화
    url = 'https://flight.naver.com/'

    browser.get(url) # url로 이동
    sleep(3)

    # 목적지 선택을 위한 클릭
    # !! class 이름에 공백이 들어가는 경우 '.' 으로 대체해줘야한다.
    browser.find_element(By.XPATH, '//b[text() = "도착"]').click()

    sleep(1)

    # 목적지 검색 창 선택
    browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").click()
    sleep(1)
    browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").send_keys("런던")
    sleep(1)

    # 첫번째 선택
    browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()
    print("선택 성공")

    ## 일정 선택
    # 가는 날
    browser.find_element(By.XPATH, '//button[text() = "가는 날"]').click()
    sleep(1)
    browser.find_elements(By.XPATH, '//b[text() = "27"]')[0].click()

    # 오는 날 
    browser.find_element(By.XPATH, '//button[text() = "오는 날"]').click()
    sleep(1)
    browser.find_elements(By.XPATH, '//b[text() = "6"]')[1].click()

    sleep(1)

    # 검색 버튼 누르기
    browser.find_element(By.XPATH, '//span[text() = "항공권 검색"]').click()


    # browser.implicitly_wait(10)

    sleep(10)


    # 검색 결과 창이 나오면 직항/경우 버튼 클릭 
    browser.find_element(By.XPATH, '//span[text() = "직항/경유 "]').click()



    # 버튼 클릭 후 박스가 내려오면 직항과 경우 최저가를 기록
    direct_flight_price = browser.find_elements(By.CLASS_NAME, 'filter_num__2LIP9')[0].text
    indirect_flight_price = browser.find_elements(By.CLASS_NAME, 'filter_num__2LIP9')[1].text




    for idx, day in enumerate(day_depart): 
        





