import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "functions"))
from datetime import datetime
from functions.header import *
from functions import Youtube_Linkgetter
from functions import Youtube_Commentgetter
from functions import SortComments
from functions.GetLabel import *

# tfidf를 불러다 쓰기 위해 필요한 친구들
def preprocessor(text):
    text = re.sub("\W+", ' ', text)     # remove all non-words
    text = re.sub("^\s", '', text)      # remove space in start of the statement
    text = re.sub("\s$", '', text)      # remove space in end of the statement
    return text

# 텍스트를 처리하기 위해 Okt 사용
okt = Okt()
def tokenizer_kor(text) :
    return okt.morphs(text, stem = True, norm = True)


if __name__ == "__main__" :
    ### 검색어
    # 기본
    # search_list = ["징역", "처벌"]
    # 원하는 값이 있을 경우
    search_list = ["부산 돌려차기"]

    ### 라벨
    # 기본
    # label = datetime.today().strftime("%Y-%m-%d")
    # 원하는 값이 있을 경우
    label = "마라샹궈 쿡방"

    ### 필터 목록
    # 기본
    filter = "&sp=EgIQAQ%253D%253D"
    # 1일 이내만  
    # filter = "&sp=EgQIAhAB"
    
    # Youtube_Linkgetter.linkGetter(search_list = search_list, label = label, filter = filter, finish_line = 15000, flag = False)

    link = "https://www.youtube.com/watch?v=kNcEIG_6hJs"
    # Youtube_Commentgetter.commentGetter(label = label)
    Youtube_Commentgetter.commentGetter_single(link = link, label = label)

    # SortComments.sortComments(label = label)

    getLabel(label, flag = False)