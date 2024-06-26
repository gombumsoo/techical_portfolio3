import os
import time
import socket

from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from PIL import Image
from pygame import mixer

#스크롤 내려주는 함수
def scroll_down():
    scroll_count = 0

    print("ㅡ 스크롤 다운 시작 ㅡ")

    # 스크롤 위치값 얻고 last_height 에 저장
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 결과 더보기 버튼을 클릭했는지 유무
    after_click = False

    while True:
        print(f"ㅡ 스크롤 횟수: {scroll_count} ㅡ")
        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1
        time.sleep(1)

        # 스크롤 위치값 얻고 new_height 에 저장
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 스크롤이 최하단이며
        if last_height == new_height:

            # 결과 더보기 버튼을 클릭한적이 있는 경우
            if after_click is True:
                print("ㅡ 스크롤 다운 종료 ㅡ")
                break

            # 결과 더보기 버튼을 클릭한적이 없는 경우
            if after_click is False:
                if driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').is_displayed():
                    driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
                    after_click = True
                elif NoSuchElementException:
                    print("ㅡ NoSuchElementException ㅡ")
                    print("ㅡ 스크롤 다운 종료 ㅡ")
                    break
        last_height = new_height


#썸네일 이미지를 클릭하면 우측에 뜨는 원본 이미지를 urlretrieve(저장)하는 함수
def click_and_retrieve(index, img, img_list_length):
    global crawled_count
    try:
        img.click()
        driver.implicitly_wait(3)
        src = driver.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute('src')
        if src.split('.')[-1] == "png":
            urlretrieve(src, path + date + '/' + query + '/' + str(crawled_count + 1) + ".png")
            print(f"{index + 1} / {img_list_length} 번째 사진 저장 (png)")
        else:
            urlretrieve(src, path + date + '/' + query + '/' + str(crawled_count + 1) + ".jpg")
            print(f"{index + 1} / {img_list_length} 번째 사진 저장 (jpg)")
        crawled_count += 1

    except HTTPError:
        print("ㅡ HTTPError & 패스 ㅡ")
        pass



#위에서 만든 함수 scroll_down()과 click_and_retrieve()를 호출하며 다양한 예외처리를 하는 함수
def crawling():
    global crawled_count

    print("ㅡ 크롤링 시작 ㅡ")

    # 이미지 고급검색 중 이미지 유형 '사진'
    url = f"https://www.google.com/search?as_st=y&tbm=isch&hl=ko&as_q={query}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:photo"
    driver.get(url)
    driver.maximize_window()
    scroll_down()

    div = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]')
    # class_name에 공백이 있는 경우 여러 클래스가 있는 것이므로 아래와 같이 css_selector로 찾음
    img_list = div.find_elements_by_css_selector(".rg_i.Q4LuWd")
    os.makedirs(path + date + '/' + query)
    print(f"ㅡ {path}{date}/{query} 생성 ㅡ")

    for index, img in enumerate(img_list):
        try:
            click_and_retrieve(index, img, len(img_list))

        except ElementClickInterceptedException:
            print("ㅡ ElementClickInterceptedException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(index, img, len(img_list))

        except NoSuchElementException:
            print("ㅡ NoSuchElementException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(index, img, len(img_list))

        except ConnectionResetError:
            print("ㅡ ConnectionResetError & 패스 ㅡ")
            pass

        except URLError:
            print("ㅡ URLError & 패스 ㅡ")
            pass

        except socket.timeout:
            print("ㅡ socket.timeout & 패스 ㅡ")
            pass

        except socket.gaierror:
            print("ㅡ socket.gaierror & 패스 ㅡ")
            pass

        except ElementNotInteractableException:
            print("ㅡ ElementNotInteractableException ㅡ")
            #break
            pass

    try:
        print("ㅡ 크롤링 종료 (성공률: %.2f%%) ㅡ" % (crawled_count / len(img_list) * 100.0))

    except ZeroDivisionError:
        print("ㅡ img_list 가 비어있음 ㅡ")

    driver.quit()


#다운로드한 이미지의 해상도가 100x100 이하이던가 손상된 이미지라면 삭제하는 함수
def filtering():
    print("ㅡ 필터링 시작 ㅡ")
    filtered_count = 0
    dir_name = path + date + '/' + query
    for index, file_name in enumerate(os.listdir(dir_name)):
        try:
            file_path = os.path.join(dir_name, file_name)
            img = Image.open(file_path)

            # 이미지 해상도의 가로와 세로가 모두 100이하인 경우
            if img.width < 100 and img.height < 100:
                img.close()
                os.remove(file_path)
                print(f"{index} 번째 사진 삭제")
                filtered_count += 1

        # 이미지 파일이 깨져있는 경우
        except OSError:
            os.remove(file_path)
            filtered_count += 1

    print(f"ㅡ 필터링 종료 (총 갯수: {crawled_count - filtered_count}) ㅡ")


#입력받은 검색어가 중복인지 판단하는 함수
def checking():
    # 입력 받은 검색어가 이름인 폴더가 존재하면 중복으로 판단
    for dir_name in os.listdir(path):
        file_list = os.listdir(path + dir_name)
        if query in file_list:
            print(f"ㅡ 중복된 검색어 ({dir_name}) ㅡ")
            return True

#mp3를 재생하는 함수 (크롤링이 끝났다는 것을 알리기 위함)
def playing_mp3():
    mp3 = "Mococo_Seed.mp3"
    mixer.init()
    mixer.music.load(mp3)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    print(f"ㅡ 검색어: {query} ㅡ")


# clickAndRetrieve() 과정에서 urlretrieve 이 너무 오래 걸릴 경우를 대비해 타임 아웃 지정
socket.setdefaulttimeout(50)

# 이미지들이 저장될 경로 및 폴더 이름
path = "경로"
date = "날짜"

# 드라이버 경로 지정 (Microsoft Edge)
driver = webdriver.Chrome("드라이버/경로")   

# 크롤링한 이미지 수
crawled_count = 0

# 검색어 입력 받기
query = input("입력: ")
# 이미 크롤링했던 검색어일 때
while checking() is True:
    query = input("입력: ")

crawling()
filtering()
playing_mp3()
