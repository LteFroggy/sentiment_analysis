import os
import sys
sys.path.append(os.path.dirname(__file__))
from header import *

# 열린 browser와 link를 받아서 댓글을 반환해주는 함수
def getYoutubeComments(browser, link) :
    # 댓글 저장할 공간 만들기
    commentList = []

    # 링크 열기
    browser.get(link)
    time.sleep(4)

    # 스크롤 끝까지 내리기
    last_scroll_height = browser.execute_script("return document.documentElement.scrollHeight")
    while True :
        # 한 페이지 내리기
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        # 새 높이 받아오기
        new_scroll_height = browser.execute_script("return document.documentElement.scrollHeight")

        # 새 높이 = 기존 높이이면 다 내린 것. 그만하기
        if (last_scroll_height == new_scroll_height) :
            break
        # 아니면 더 내리기
        else :
            last_scroll_height = new_scroll_height


    #### 답글창은 싸움장일 확률이 높음. 일단 가져올지 말지는 천천히 고민하자.
    # # 스크롤을 다 내렸다면 대댓글창 모두열기
    # try :
    #     # 답글이 하나도 없으면 오류 날 수 있으므로 try - except
    #     reply_buttons = browser.find_elements_by_xpath("//*[@id='more-replies']")
    #     print("대댓글 보기 총", str(len(reply_buttons)) + "개 발견")
    #     for button in reply_buttons :
    #         browser.execute_script("arguments[0].click()", button)
    #         time.sleep(2)
    #         # 너무 답글이 많으면 답글 더보기가 나올수도 있음. 이것까지 처리하기
    #         while True :
    #             additional_button = browser.find_elements_by_xpath('//*[@id="button"]/ytd-button-renderer/yt-button-shape/button')
    #             if (len(additional_button) != 0) :
    #                 browser.execute_script("arguments[0].click()", additional_button[0])
    #                 time.sleep(2)
    #             else :
    #                 break
    # except Exception as E :
    #     print("에러 발생 : " + str(E))

    # HTML로 긁어오기
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'lxml')

    # 댓글별로 div 가져오기
    commentList_html = soup.find_all("ytd-comment-renderer", attrs = {"id" : "comment", "class" : "style-scope ytd-comment-thread-renderer"})
    
    # 댓글이 없는 경우 아무것도 돌려주지 않기
    if len(commentList_html) == 0 :
        return None

    # div별 분석
    for comment in commentList_html :
        # 작성 유저명, 내용, 추천수 가져오기
        try :
            userName = comment.find("span", attrs = {"class" : "style-scope ytd-comment-renderer style-scope ytd-comment-renderer"}).text
            content = comment.find("yt-formatted-string", attrs = {"id" : "content-text", "class" : "style-scope ytd-comment-renderer"}).text
            voteCount = comment.find("span", attrs = {"id" : "vote-count-middle", "class" : "style-scope ytd-comment-action-buttons-renderer"}).text
        except :
            continue

        # 가져온 값 전부 공백 제거
        userName = removeSpaces(userName)
        content = removeSpaces(content)
        voteCount = removeSpaces(voteCount)

        # 이상하게 유저명 앞에 전부 @가 끼어있어서 이것도 제거
        userName = re.sub("^@", "", userName)

        tmp = []
        tmp.append(userName)
        tmp.append(content)
        tmp.append(voteCount)

        commentList.append(tmp)

    return commentList

def commentGetter(label = today) :
    # 에러 해결용 코드
    # USB: usb_service_win.cc:415 Could not read device interface GUIDs: 지정된 파일을 찾을 수 없습니다. (0x2)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # label에 맞는 csv파일 불러와서 numpy로 만들기
    df = pd.read_csv(os.path.join(linkPath, label + ".csv"))
    videoList = df.to_numpy()

    # 파일 저장할 폴더 만들기
    dataSavingPath = os.path.join(dataPath, label)
    if not os.path.isdir(dataSavingPath) :
        os.mkdir(dataSavingPath)        

    # 크롬드라이버 실행
    driver_path = "./chromedriver.exe"
    browser = webdriver.Chrome(executable_path = driver_path, options = options)
    browser.maximize_window()

    # 불러온 비디오리스트에 대해 수행
    for name, channel, link in videoList :
        # 함수를 통해 링크별 댓글 따오기 
        comments = getYoutubeComments(browser, link)
        
        # 댓글이 없는 게시물일 경우 넘기기
        if comments == None :
            continue
        
        # 데이터프레임으로 변환
        df_comments = pd.DataFrame(comments, columns = ["작성자", "내용", "추천수"])

        # 파일명에 특수문자 없애기
        name_new = re.sub("\W+", " ", name)
        # 파일명에 띄어쓰기도 문제가 발생할 수 있으므로 언더바로 대체
        name_new = re.sub("\s+", "_", name_new)
        # 파일명이 너무 길면 join이 잘 안되는 듯 함. 30자만 적기
        name_new = name_new[:30]

        # datas폴더에 label별로 넣어서 저장
        df_comments.to_csv(os.path.join(dataSavingPath, name_new + ".csv"), mode = 'w', index = False)

if __name__ == "__main__" :
    commentGetter("돌려차기")