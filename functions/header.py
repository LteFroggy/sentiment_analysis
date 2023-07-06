import os
import re
import sys
import time
import requests
import matplotlib
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import pyplot as plt
# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.keys import Keys

today = datetime.today().strftime("%Y-%m-%d")
rootPath = os.getcwd()
currentPath = os.path.dirname(__file__)
linkPath = os.path.join(rootPath, "link")
dataPath = os.path.join(rootPath, "datas")
resultPath = os.path.join(rootPath, "result")


def removeSpaces(state) :
    # �յ� ���� ����
    state = re.sub("^\s+", "", state)
    state = re.sub("\s+$", "", state)

    # �߰� �������� �����̳� Ȥ�� �ٹٲ� �� ��� ���� ��ĭ���� ��ü
    state = re.sub("\s+", " ", state)

    return state