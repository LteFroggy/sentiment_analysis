import os
import sys
import platform
from math import log
sys.path.append(os.path.dirname(__file__))
from header import *

label = "가평계곡"

# result내에 저장되어있는 댓글들의 긍정, 부정 정도를 먼저 판단
filePath = os.path.join(resultPath, label + ".csv")
nArray = pd.read_csv(filePath, encoding = 'utf-8').to_numpy()

positive_list = np.array([a for a in nArray if a[1] == 1])
negative_list = np.array([a for a in nArray if a[1] == 0])

print(f"Positive's Shape : {positive_list.shape}")
print(f"Negative's Shape : {negative_list.shape}")

print(positive_list[0])

# 추천수를 로그 스케일로 고려하여 갯수에 반영
# positive_count = [round(log(2 + int(comment[2], 2)), 1) for comment in positive_list]
# negative_count = [round(log(2 + int(comment[2], 2)), 1) for comment in negative_list]

positive_count = 0
negative_count = 0
for comment in positive_list :
    # print(f"댓글 전체 : {comment}")
    try :
        positive_count += round(log(2 + int(comment[2]), 2))
        # print(f"추천수 {comment[2]}개, 로그스케일 적용 시 {round(log(2 + int(comment[2]), 2))}개")
    except ValueError :
        # 추천수가 1,000 개가 넘으면 "1천"등으로 표기되어서 오류가 남. 이 경우에는 그냥 더해주기
        positive_count += 10

for comment in negative_list :
    # print(f"댓글 전체 : {comment}")
    try :
        negative_count += round(log(2 + int(comment[2]), 2))
        # print(f"추천수 {comment[2]}개, 로그스케일 적용 시 {round(log(2 + int(comment[2]), 2))}개")
    except ValueError :
        # 추천수가 1,000 개가 넘으면 "1천"등으로 표기되어서 오류가 남. 이 경우에는 그냥 더해주기
        negative_count += 10

print(positive_count)
print(negative_count)

# Ratio 지정
ratio = [positive_count, negative_count]

# label 지정
plt_label = ["Positive", "Negative"]

# 그래프에 한글 출력이 가능하도록 만들기
# Window
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
# Mac
elif platform.system() == 'Darwin': 
    matplotlib.rc('font', family='AppleGothic')

plt.title("Response About " + label)
plt.pie(ratio, labels = plt_label, autopct = '%.2f')
plt.show()

