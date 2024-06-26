import os
from time import sleep
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#'부산 강서구', '부산 금정구', '부산 기장군', ' 부산 남구', '부산 동구', '동래구', '부산 진구', '부산 북구', '부산 사상구', '부산 사하구', '부산 서구', '부산 수영구', '부산 연제구', '부산 영도구', '부산 해운대구', '부산 중구'

# 서울특별시 구 리스트 
busan_gu_list = ['부산 동구']

#search_list 배열에 검색키워드를 적어주세요.
search_list = ['고등학교']

for index, store_name in enumerate(search_list):
    #fileName = store_name + ''
    fileName = f'fuck/{store_name}.csv'
    file = open(fileName, 'w', encoding='utf-8')
    file.write("매장명" + "|" + "주소" + "|"  + "\n")
    file.close()

    for index, gu_name in enumerate(busan_gu_list):

        options = webdriver.ChromeOptions()
        options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36   ")
        options.add_argument('lang=ko_KR')
        chromedriver_path = "C://chromedriver_win32/chromedriver.exe"
        driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기
        driver.get('https://map.kakao.com/')  # 주소 가져오기
        search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]') # 검색 창
        search_area.send_keys(gu_name + ' ' +store_name)  # 검색어 입력
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        driver.implicitly_wait(3)
        time.sleep(1)
        more_page = driver.find_element_by_id("info.search.place.more")
        place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li')
        no_place = driver.find_element_by_id("info.noPlace")

        # 검색결과가 없을 때
        if 'HIDDEN' not in no_place.get_attribute('class'):
            continue

        # 더보기 버튼이 있을 때
        if 'HIDDEN' not in  more_page.get_attribute('class'):
            print("더보기 있음")
            more_page.send_keys(Keys.ENTER) # 더보기 버튼 선택
        # 더보기 버튼이 없을 때 (검색결과가 적을 때)
        else:
            file = open(fileName, 'a', encoding='utf-8')
            for p in place_lists: # WebElement
                store_html = p.get_attribute('innerHTML')
                store_info = BeautifulSoup(store_html, "html.parser")
                place_name = store_info.select('.head_item > .tit_name > .link_name')
                if len(place_name) == 0:
                    continue # 광고
                
                place_naming = store_info.select('.head_item > .tit_name > .link_name')[0].text
                place_address = store_info.select('.info_item > .addr > p')[0].text
            
                if gu_name not in place_address :
                    continue
                    
                file.write(place_naming + "|" + place_address + "\n")
            continue

        time.sleep(1)

        Page = 1

        while True: # 다음 페이지가 있으면 loop
            file = open(fileName, 'a', encoding='utf-8')
            time.sleep(1)
            page_links = driver.find_elements_by_css_selector("#info\.search\.page a")
            pages = [link for link in page_links if "HIDDEN" not in link.get_attribute("class").split(" ")]
            print(len(pages), "개의 페이지 있음")
            # pages를 하나씩 클릭하면서
            for i in range(1, len(pages) + 1):
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                try:
                    page = driver.find_element_by_xpath(xPath)
                    page.send_keys(Keys.ENTER)
                except ElementNotInteractableException:
                    print('마지막 페이지')
                    break;
                sleep(3)
                place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li')
                for p in place_lists: # WebElement

                    store_html = p.get_attribute('innerHTML')
                    store_info = BeautifulSoup(store_html, "html.parser")

                    place_name = store_info.select('.head_item > .tit_name > .link_name')
                    if len(place_name) == 0:
                        continue # 광고
                        
                    #if place_address_element:
                    #place_address_dong = place_address_element['title']

                    place_name = store_info.select('.head_item > .tit_name > .link_name')[0].text
                    place_address = store_info.select('.info_item > .addr > p')[0].text
                    if gu_name not in place_address :
                        continue

                    file.write(place_name + "|" + place_address + "\n")
                print(i, ' of', ' [ ' , Page, ' ] ')
                #print(store_info)#gg
                
            next_btn = driver.find_element_by_id("info.search.page.next")
            has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
            if not has_next:
                print('다음페이지 x')
                driver.close()
                file.close()
                break # 다음 페이지 없으니까 종료
            else: # 다음 페이지 있으면
                Page += 1
                next_btn.send_keys(Keys.ENTER)
        print("종료")