import sys
import os
from datetime import datetime
from functions import Youtube_Linkgetter
from functions import Youtube_Commentgetter

# sys.path.append(os.path.join(os.path.dirname(__file__), "functions"))

if __name__ == "__main__" :
    ### 검색어
    # 기본
    # search_list = ["징역", "처벌"]
    # 원하는 값이 있을 경우
    search_list = ["이은해 구형"]

    ### 라벨
    # 기본
    # label = datetime.today().strftime("%Y-%m-%d")
    # 원하는 값이 있을 경우
    label = "가평계곡"

    ### 필터 목록
    # 기본
    filter = "&sp=EgIQAQ%253D%253D"
    # 1일 이내만  
    # filter = "&sp=EgQIAhAB"
    
    Youtube_Linkgetter.linkGetter(search_list = search_list, label = label, filter = filter, finish_line = 10000)

    Youtube_Commentgetter.commentGetter(label = label)