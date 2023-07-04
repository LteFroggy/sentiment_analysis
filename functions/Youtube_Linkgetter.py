import os
import sys
sys.path.append(os.path.dirname(__file__))
from header import *

# 검색어 목록
search_list = ["징역", "처벌"]

# 1일 내에 올라온 게시물만 보이도록 하는 필터
filter = "&sp=EgIIAg%253D%253D"

# 스크롤을 어디까지 내릴지
finish_line = 5000

def linkGetter(search_list = search_list, filter = filter, finish_line = finish_line, label = today, flag = True) :
    # 에러 해결용 코드
    # USB: usb_service_win.cc:415 Could not read device interface GUIDs: 지정된 파일을 찾을 수 없습니다. (0x2)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 접속할 URL
    url = "https://www.youtube.com"

    # 이름, 게시자, 링크의 저장공간 만들기
    videoList = []

    driver_path = "./chromedriver.exe"
    browser = webdriver.Chrome(executable_path = driver_path, options = options)
    browser.maximize_window()
    browser.get(url)

    for search_word in search_list :
        # 검색창 찾기
        search = browser.find_element_by_name("search_query")
        search.clear()
        time.sleep(2)

        # 검색어 쓰고 엔터치기
        search.send_keys(search_word)
        search.send_keys(Keys.ENTER)
        time.sleep(2)

        # 1일 이내 게시물만 보이도록 링크 수정
        browser.get(browser.current_url + filter)
        time.sleep(2)

        # 원하는데까지 스크롤을 내려야 영상이 로딩됨
        last_page_height = browser.execute_script("return document.documentElement.scrollHeight")
        print("처음 페이지 높이 : ", last_page_height)

        # 원하는 위치까지 먼저 스크롤 내리기
        while True :
            # 일단 스크롤 내리기
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # 잠깐 쉬어서 로딩시간 확보
            time.sleep(2)

            # 현재 위치 담기
            new_page_height = browser.execute_script("return document.documentElement.scrollHeight")

            if new_page_height > finish_line :
                break
            else :
                last_page_height = new_page_height
                print("새 페이지 높이 : ", last_page_height)

        # 페이지 다 내렸다면 bs4를 이용해 가져오기
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'lxml')


        # 하나의 영상을 나타내는 단위가 ytd-video-renderer이므로 이걸 다 찾아서 저장
        videoList_html = soup.find_all("ytd-video-renderer", {"class" : "style-scope ytd-item-section-renderer"})

        for video in videoList_html :
            # 링크, 이름, 채널명 찾아오기
            video_link = video.find("a", {"id" : "video-title", "class" : "yt-simple-endpoint style-scope ytd-video-renderer"})["href"]
            video_name = video.find("yt-formatted-string", {"class" : "style-scope ytd-video-renderer"}).text
            channel_name = video.find("tp-yt-paper-tooltip", {"class" : "style-scope ytd-channel-name"}).text

            # 쇼츠라면 리스트에 넣지 않기
            if (video_link[:7] == "/shorts") :
                continue
            else :
                video_link = "https://www.youtube.com" + video_link

            # 이름에 키워드가 없으면 넣지 않기
            # 키워드가 좀 복잡한 경우 없을 확률이 높음. 이건 flag값을 false로 줘서 조정
            if(flag and re.search(search_word, video_name) == None) :
                continue

            # 채널명에 공백 제거
            channel_name = removeSpaces(channel_name)

            tmp = []
            tmp.append(video_name)
            tmp.append(channel_name)
            tmp.append(video_link)

            # 중복되는 게시물이 이미 등록되었다면 넣지 않기
            if (tmp not in videoList) :
                videoList.append(tmp)

    # 다 찾았으면 df로 변경
    videoList = pd.DataFrame(videoList, columns = ["영상제목", "채널명", "링크"])
    print(videoList)

    # 날짜에 맞게 저장
    videoList.to_csv(os.path.join(linkPath, label + ".csv"), mode = 'w', index = False)


if __name__ == "__main__" :
    search_list = ["돌려차기"]
    label = "돌려차기"
    filter = "&sp=EgIQAQ%253D%253D"
    # 필터 목록
    # 1일 이내만  &sp=EgQIAhAB
    # 기본        &sp=EgIQAQ%253D%253D

    linkGetter(search_list = search_list, filter = filter, finish_line = 20000, label = label)