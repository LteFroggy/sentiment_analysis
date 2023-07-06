import os
import sys
sys.path.append(os.path.dirname(__file__))
import re
import pickle
import numpy as np
import pandas as pd
from header import *
from konlpy.tag import Okt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

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

# 먼저 필터링된 댓글 다 한군데에 모으기
label = "가평계곡"

def getLabel(label = label) :
    # 경로부터 지정
    targetPath = os.path.join(dataPath, label+"_filtered")

    # 내부에 있는 모든 파일 리스팅
    fileList = os.listdir(targetPath)

    # 파일별로 댓글 뽑아오기
    comments = []
    for file in fileList :
        data = pd.read_csv(os.path.join(targetPath, file), encoding = 'utf-8').values.tolist()
        comments += data

    comments = np.array(comments)

    # 어떤 유저가 쓴 댓글인지는 별 상관 없을 듯? 닉네임 지우기
    comments = comments[:, 1:]
    print(comments[:5])

    modelPath = os.path.join(rootPath, "model")

    # 필요한 tfidf, model 불러오기
    with open(os.path.join(modelPath, 'tfidf.pkl'), 'rb') as f :
        tfidf = pickle.load(f)

    with open(os.path.join(modelPath, 'linear_model.pkl'), 'rb') as f :
        lr = pickle.load(f)


    # tfidf로 전처리 후 댓글별 찬성, 반대 의견 넣어주기
    content = comments[:, [0]]
    content = np.squeeze(content)

    print(content[:5])
    print(content.shape)

    data_vector = tfidf.transform(content)
    data_vector = data_vector.toarray()

    print("벡터화 완료")

    y_pred = lr.predict(data_vector)

    print("예측 완료")

    content = content.reshape(-1, 1)
    y_pred = y_pred.reshape(-1, 1)
    result = np.concatenate((content, y_pred), axis = 1)
    result = np.concatenate((result, comments[:, [1]]), axis = 1)

    ### 결과를 저장하기
    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(result, columns = ["내용", "판단 결과", "추천수"])

    # 저장할 경로 설정
    resultPath = os.path.join(rootPath, "result")
    dataSavePath = os.path.join(resultPath, label + ".csv")
    df.to_csv(dataSavePath, mode = "w", index = False)