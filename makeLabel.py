import re
import os
import sys
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.keys import Keys

# label에는 새로 라벨링하려 하는 값 넣기
label = "가평계곡"

rootPath = os.getcwd()
resultPath = os.path.join(rootPath, "result")
nArray = pd.read_csv(os.path.join(resultPath, label + ".csv"), encoding = 'utf-8').to_numpy()
lst = nArray.tolist()

# 기존에 분류하던 게 있으면 그대로 두고, 아니면 이동하기
try :
    old = pd.read_csv("./가평계곡_newLabel.csv").to_numpy()
    startPoint = old.shape[0]
    labeled = old.tolist()
except Exception as E:
    print("Error :", E)
    startPoint = 0
    labeled = []
    
savePath = os.path.join(rootPath, label + "_newLabel.csv")

while startPoint < nArray.shape[0] :
    if (startPoint % 10 == 0) :
        df = pd.DataFrame(labeled, columns = ["내용", "라벨", "추천수"])
        df.to_csv(savePath, index = False)
        print(f"{startPoint}번째 진입으로 중간 저장 완료")

    print(f"{startPoint}번째 댓글입니다")
    temp = nArray[startPoint]
    print(temp[0])
    if temp[1] == 1 :
        print("부정적이지 않은 댓글입니다")
    else :
        print("부정적인 댓글입니다")

    result = input("맞으면 1, 아니면 2를 입력해주세요. 관련이 없는 댓글이라면 3을 눌러주세요 : ")

    if (result == '1') :
        labeled.append(temp)
        print("그대로 저장하였습니다.", end = "\n\n")
        startPoint += 1

    elif (result == '2') :
        temp[1] = 1 if temp[1] == '0' else 0
        labeled.append(temp)
        print("라벨을 바꾸어 저장하였습니다.", end = "\n\n")
        startPoint += 1
    
    elif (result == '3') :
        print("넘겼습니다.", end = "\n\n")
        temp[1] = 3
        labeled.append(temp)
        startPoint += 1
    
    else :
        print("잘못 입력하셨습니다. 다시 시도해주세요", end = "\n\n")