import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
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

if __name__ == "__main__":

    # 출발 일자 리스트 정리 
    depart_day_all, ls_depart, back_day_all, ls_back = def_.ready(28+214) # core.txt에서 인덱스 58에서 끊겼으면 def_.ready(28+59) # 아래에 바꿔줘야할 것 더 있음

    back_day_all = back_day_all.tolist() # 밑에서 리스트.pop(0) 을 쓰기 위해 numpy 형식이었던 것을 list로 바꿔줌


    print(len(depart_day_all), len(ls_depart), len(back_day_all), len(ls_back)) # 값이 모두 같아야함


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
    sleep(2)

    # 첫번째 선택
    browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()

    sleep(2)

    direct_price_ls = []
    indirect_price_ls = []

    for idx, day in enumerate(depart_day_all): 

        # 가는 날
        browser.find_elements(By.CLASS_NAME, 'tabContent_option__2y4c6.select_Date__1aF7Y')[0].click()
        sleep(1)
        browser.find_elements(By.XPATH, f'//b[text() = "{day}"]')[ls_depart[idx]].click()
        print(day, ls_depart[idx])
        sleep(1)

        # 오는 날 
        browser.find_elements(By.CLASS_NAME, 'tabContent_option__2y4c6.select_Date__1aF7Y')[1].click()
        sleep(2)
        
        try:
            browser.find_elements(By.XPATH, f'//b[text() = "{back_day_all[idx]}"]')[ls_back[idx]].click()
        except:
            try:
                browser.find_elements(By.XPATH, f'//b[text() = "{back_day_all[idx]}"]')[ls_back[idx]].click()
            except:
                raise ValueError
        print(back_day_all[idx], ls_back[idx])
        # back_day_all.pop(0)
        sleep(2)

        # 검색 버튼 누르기
        browser.find_element(By.XPATH, '//span[text() = "항공권 검색"]').click()


        # 페이지에서 직항/경유 버튼 나올 때까지 대기 
        WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, '//span[text() = "직항/경유 "]')))


        # 직항이 없을 경우 예외처리
        # 직항 가격을 0 으로 수집 
        try:
            # 직항/경유 버튼 클릭
            browser.find_element(By.XPATH, '//span[text() = "직항/경유 "]').click()
            sleep(1)
            # 직항 클릭 
            browser.find_element(By.XPATH, '//i[text() = "직항"]').click()
            sleep(1)
            # 적용 클릭
            browser.find_element(By.XPATH, '//button[text() = "적용"]').click()
            # 첫번째 가격정보 가져오기
            elem_direct = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//div[@class="concurrent_ConcurrentItemContainer__2lQVG result"]')))

            direct_price_ls.append((idx+214, elem_direct.text))
        except:
            direct_price_ls.append((idx+214, 0))


        # 경유가 없을 경우 예외처리
        # 경유 가격을 0으로 수집 
        try:
            # 직항/ 경유 버튼 클릭
            browser.find_element(By.XPATH, '//span[text() = "직항/경유 "]').click()
            sleep(1)
            # 직항 클릭(이미 적용되어있는 직항항목을 삭제하기위해) 
            browser.find_element(By.XPATH, '//i[text() = "직항"]').click()
            sleep(1)
            # 경유 1회 클릭
            browser.find_element(By.XPATH, '//i[text() = "경유 1회"]').click()
            sleep(1)
            # 적용 클릭
            browser.find_element(By.XPATH, '//button[text() = "적용"]').click()
            # 페이지에서 첫번째 가격정보 데이터 나올때까지 대기 
            elem_indirect = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//div[@class = "concurrent_ConcurrentItemContainer__2lQVG result"]')))

            indirect_price_ls.append((idx+214, elem_indirect.text))

        except:
            indirect_price_ls.append((idx+214, 0))

        print(f"[{direct_price_ls[-1]}&&&&&{indirect_price_ls[-1]}],") # 가장 최근에 수집한 직항 & 경우 데이터 수집 


        # 메모장에 기록
        with open('./core.txt', 'a') as core:
            core.write(f"[{direct_price_ls[-1]}&&&&&{indirect_price_ls[-1]}],\n")







        ## 일정 횟수 반복해서 스크래핑할 경우 목적지 기본 셋팅을 상실하는 경우가 있다.
        # 따라서 목적지를 항상 기입해주는 방향으로 전개.

        # 목적지 버튼 클릭
        browser.find_elements(By.CLASS_NAME, 'select_code__d6PLz')[1].click()

        # 목적지 검색 창 선택
        browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").click()
        sleep(1)
        try:
            browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").send_keys("런던")
            sleep(1)

            # 첫번째 선택
            browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()
        except:
            try:
                # 목적지 버튼 클릭
                browser.find_elements(By.CLASS_NAME, 'select_code__d6PLz')[1].click()
                # 목적지 검색 창 선택 # 오류를 살펴보니 검색창이 활성화 안되는경우도 존재해서 예외처리로 클릭을 눌러준다.
                browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").click()
                sleep(1)
                browser.find_element(By.XPATH, "//input[@class='autocomplete_input__1vVkF']").send_keys("런던")
                sleep(1)

                # 첫번째 선택
                browser.find_element(By.XPATH, '//i[text() = "히드로공항"]').click()
            except:
                pass

        sleep(1)
