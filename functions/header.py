import os
import re
import sys
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

today = datetime.today().strftime("%Y-%m-%d")
rootPath = os.getcwd()
currentPath = os.path.dirname(__file__)
linkPath = os.path.join(rootPath, "link")
dataPath = os.path.join(rootPath, "datas")


def removeSpaces(state) :
    # �յ� ���� ����
    state = re.sub("^\s+", "", state)
    state = re.sub("\s+$", "", state)

    # �߰� �������� �����̳� Ȥ�� �ٹٲ� �� ��� ���� ��ĭ���� ��ü
    state = re.sub("\s+", " ", state)

    return state