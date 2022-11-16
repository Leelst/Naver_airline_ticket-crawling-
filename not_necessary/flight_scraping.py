import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import def_

# selenium 최신버전 문법이 바뀌어서 기존의 문법으로 이용하려면 selenium 3.14.1 버전 설치
# pip install selenium==3.14.1

# 이번엔 최신 버전의 selenium 문법 이용
# pip install selenium

"-------------------------------------------------------------------------------------------------------------------"

## 일정 정리
    ## 런던의 경우 9박 10일 일정을 계획 ## 
    ## 가는 날 리스트만들기 (22년 9월 28일부터 23년 8월월 31일까지)##

# 출발 일자 리스트 정리 
depart_day_all, ls_depart, back_day_all, ls_back = def_.ready(28)


print(len(depart_day_all), len(ls_depart), len(back_day_all), len(ls_back))


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True) # 크롬창 자동으로 꺼지는 것 막는 용도
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


browser.maximize_window() # 창 최대화
url = 'https://flight.naver.com/'
browser.get(url) # url로 이동
sleep(3)

browser.find_element(By.XPATH, '//b[text() = "도착"]').click()

sleep(1)

# 목적지 검색 창 선택
browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").click()
sleep(1)
browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").send_keys("런던")
sleep(1)

# 첫번째 선택
browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()

sleep(1)

direct_price_ls = []
indirect_price_ls = []

for idx, day in enumerate(depart_day_all): 

    # 가는 날
    browser.find_elements(By.CLASS_NAME, 'tabContent_option__2y4c6.select_Date__1aF7Y')[0].click()
    sleep(1)
    browser.find_elements(By.XPATH, f'//b[text() = "{day}"]')[ls_depart[idx]].click()

    sleep(2)

    # 오는 날 
    browser.find_elements(By.CLASS_NAME, 'tabContent_option__2y4c6.select_Date__1aF7Y')[1].click()
    sleep(2)
    
   
    browser.find_elements(By.XPATH, f'//b[text() = "{back_day_all[0]}"]')[ls_back[idx]].click()
    ls_back.pop(0)
    sleep(2)

    # 검색 버튼 누르기
    browser.find_element(By.XPATH, '//span[text() = "항공권 검색"]').click()


    # browser.implicitly_wait(10)

    sleep(25)


    # 검색 결과 창이 나오면 직항/경우 버튼 클릭 
    try:
        browser.find_element(By.XPATH, '//span[text() = "직항/경유 "]').click()
    except: 
        pass

    sleep(1)

    # 버튼 클릭 후 박스가 내려오면 직항과 경우 최저가를 기록
    try:
        direct_flight_price = browser.find_elements(By.CLASS_NAME, 'filter_num__2LIP9')[0].text
        indirect_flight_price = browser.find_elements(By.CLASS_NAME, 'filter_num__2LIP9')[1].text

        direct_price_ls.append((idx, direct_flight_price))
        indirect_price_ls.append((idx, indirect_flight_price))
    except:
        direct_price_ls.append((idx, 0))
        indirect_price_ls.append((idx, 0))


    browser.find_elements(By.CLASS_NAME, 'select_code__d6PLz')[1].click()

    # 목적지 검색 창 선택
    browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").click()
    sleep(1)
    browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").send_keys("런던")
    sleep(1)

    # 첫번째 선택
    browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()

    sleep(1)



    print(direct_price_ls)
    print(indirect_price_ls)