import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "functions"))
from datetime import datetime
from functions.header import *
from functions import Youtube_Linkgetter
from functions import Youtube_Commentgetter
from functions import SortComments
from functions import Discriminator
from functions.GetLabel import *


###### 학습된 AI모델의 사용을 위해 필요한 부분 ######
def preprocessor(text):
    text = re.sub("\W+", ' ', text)     # remove all non-words
    text = re.sub("^\s", '', text)      # remove space in start of the statement
    text = re.sub("\s$", '', text)      # remove space in end of the statement
    return text

okt = Okt()
def tokenizer_kor(text) :
    return okt.morphs(text, stem = True, norm = True)

####################################################



if __name__ == "__main__" :

    ###### 검색 결과로 등장한 여러 영상에 대한 반응을 확인해보기 위하여 사용 ######

    ### 검색어 : 유튜브에 검색어로써 사용될 단어를 작성, 여러 검색어를 입력할 경우 각 검색어에 대한 결과를 모두 수집함
    search_list = ["이예람 중사"]

    ### 라벨 : 수집 및 분류, 결과에서 어떤 이름을 사용할 것인지를 기재
    label = "부산 돌려차기 사건"

    ### 필터 : 유튜브 링크에서 어떤 필터를 기반으로 영상들을 수집할 것인지를 작성. 기본 필터는 동영상만 결과로 나오게 설정되어있음
    # 기본(동영상만)
    filter = "&sp=EgIQAQ%253D%253D"
    # 1일 이내의 동영상만
    # filter = "&sp=EgQIAhAB"
    
    # # 웹을 열고 search_list에 작성된 값을 검색하여 링크를 link폴더 내에 저장함
    # Youtube_Linkgetter.linkGetter(search_list = search_list, label = label, filter = filter, finish_line = 15000, flag = False)

    # # link폴더 내에 저장된 csv파일을 읽고 링크에 접속하여 댓글을 수집하고 dats폴더 내에 저장.
    # Youtube_Commentgetter.commentGetter(label = label)

    # # 주제와 알맞는 댓글만 남도록 댓글을 필터링하고 datas폴더 내에 저장. 주제와 무관한 영상으로 테스트해볼 경우에는 주석처리하여 사용
    # SortComments.sortComments(label = label)

    # # model폴더 내의 tfidf.pkl과 linear_model.pkl을 불러와 댓글의 부정 여부를 판단하여 result에 저장
    # getLabel(label, flag = True)

    # 모델이 내준 결과에 추가적으로 Rule Based 분석을 수행한 후에 부정적인 댓글 비율 및 언급된 형량의 비율 도표화
    Discriminator.discriminator(label = label, preset = 10)



    ######### 링크를 이용하여 단일 영상을 분석하고자 하는 경우에 사용 ######

    # ### 라벨 : 수집 및 분류, 결과에서 어떤 이름을 사용할 것인지를 기재
    # label = ""

    # ### 링크 : 분석하고자 하는 대상이 되는 영상의 링크
    # link = ""

    # # 주어진 내에 저장된 csv파일을 읽고 링크에 접속하여 댓글을 수집하고 dats폴더 내에 저장.
    # Youtube_Commentgetter.commentGetter_single(link = link, label = label)

    # # 주제와 알맞는 댓글만 남도록 댓글을 필터링하고 datas폴더 내에 저장. 주제와 무관한 영상으로 테스트해볼 경우에는 주석처리하여 사용
    # SortComments.sortComments(label = label)

    # # model폴더 내의 tfidf.pkl과 linear_model.pkl을 불러와 댓글의 부정 여부를 판단하여 result에 저장
    # getLabel(label, flag = True)

    # # 모델이 내준 결과에 추가적으로 Rule Based 분석을 수행한 후에 부정적인 댓글 비율 및 언급된 형량의 비율 도표화
    # Discriminator.discriminator(label = label, preset = 10)