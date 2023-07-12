import os
import sys
import platform
from math import log
sys.path.append(os.path.dirname(__file__))
from header import *

label = "공군 부사관 사망사건"
preset = 10

def discriminator(label = label, preset = preset) :
    # 징역 N년 이상만 집계되도록 하기, 반어법을 사용하는 댓글들을 제거하기 위함

    # result내에 저장되어있는 댓글들의 긍정, 부정 정도를 먼저 판단
    filePath = os.path.join(resultPath, label + ".csv")
    nArray = pd.read_csv(filePath, encoding = 'utf-8').to_numpy()

    # AI의 판단에 더불어 특정 키워드가 존재할 경우 그 문장들은 긍정, 부정을 Rule Based로 판단
    positive_words = ["감사", "나이스"]
    negative_words = ["인공지능", "AI", "가족", "감형", "딸", "아들", "자녀", "자식", "선처", "모범수", "감형"]

    positive_list = []
    negative_list = []

    flag = False

    for var in nArray :
        flag = False
        # 긍정 키워드가 존재하면 긍정으로 분류
        for word in positive_words :
            if word in var[0] :
                positive_list.append(var)
                flag = True
                break
        # 부정 키워드가 존재하면 부정으로 넣기
        for word in negative_words :
            if word in var[0] :
                negative_list.append(var)
                flag = True
                break

        # 위에서 이미 리스트에 들어갔다면 스킵
        if flag :
            continue
        # 둘 다 아니였다면 라벨을 보고 결정
        elif (var[1] == 1) :
            positive_list.append(var)
        else :
            negative_list.append(var)

    positive_list = np.array(positive_list)
    negative_list = np.array(negative_list)

    print(f"Positive's Shape : {positive_list.shape}")
    print(f"Negative's Shape : {negative_list.shape}")

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
            # 추천수가 1,000 개가 넘으면 "1천"등으로 표기되어서 오류가 남. 이 경우에는 그냥 10개로 가정하고 더해주기
            negative_count += 10

    print(positive_count)
    print(negative_count)

    # Ratio 지정
    ratio = [positive_count, negative_count]

    # label 지정
    plt_label = ["Not Negative", "Negative"]

    # 그래프에 한글 출력이 가능하도록 만들기
    # Window
    if platform.system() == 'Windows':
        matplotlib.rc('font', family='Malgun Gothic')
    # Mac
    elif platform.system() == 'Darwin': 
        matplotlib.rc('font', family='AppleGothic')

    plt.title("Response About " + label)
    plt.pie(ratio, labels = plt_label, autopct = '%.2f')
    plt.savefig(os.path.join(resultPath, label + "_response.png"))

    sentense_list = []
    life_wanted = {}

    # 부정적인 댓글 중 형량을 제시하는 댓글들만 뽑아보기
    for comment in negative_list :
        # 사형 및 참수형은 하나로 통일
        find = re.search("사형|참수형", comment[0])
        if find != None :
            sentense_list.append([comment[0], "사형", comment[2]])
            continue

        find = re.search("무기징역|종신형", comment[0])
        if find != None :
            sentense_list.append([comment[0], "무기징역", comment[2]])
            continue

        find = re.findall("[\d]+년", comment[0])
        if len(find) != 0 :
            max = 0
            for years in find :
                if int(years[:-1]) > max :
                    max = int(years[:-1])

            # 기준 형량보다 낮은 값을 제시했을 경우 반어법일 확률이 높음. 넘기기
            if max <= preset :
                continue
            
            # 두 개의 차트가 만들어질 예정, 하나는 처벌 차트, 하나는 징역 차트. 그래서 징역 차트는 여기서 미리 정렬
            # 값을 하나하나 다 짚다보면 너무 값이 많아짐. 20년 단위로 끊어서 저장하기
            std = np.linspace(20, 100, 5)
            life = None
            if max >= 100 :
                life = "징역 " + str(100) + "년 이상"
            else : 
                for num in std :
                    if max <= num :
                        life = "징역 " + str(round(num)) + "년 이하"
                        break

            # 이미 분류에 있는 값이라면 추천수만큼 로그스케일로 추가시켜주기
            if life in life_wanted.keys() :
                try :
                    life_wanted[life] += round(log(2 + int(comment[2]), 2))
                except :
                    life_wanted[life] += 10
            else :
                try :
                    life_wanted[life] = round(log(2 + int(comment[2]), 2))
                except :
                    life_wanted[life] = 10

            sentense_list.append([comment[0], "징역", comment[2]])
            continue

    sentense_list = np.array(sentense_list)
    print(sentense_list.shape)
    print(sentense_list)

    sentense_wanted = {}

    # 뽑힌 결과 바탕으로 원하는 처벌 수위 확인
    for val in sentense_list :
        print(val)
        content = val[0]
        sentense = val[1]
        recommend_count = val[2]

        # 이미 분류에 있는 값이라면 추천수만큼 로그스케일로 추가시켜주기
        if sentense in sentense_wanted.keys() :
            try :
                sentense_wanted[sentense] += round(log(2 + int(recommend_count), 2))
            except :
                sentense_wanted[sentense] += 10
        # 없는 값이라면 분류를 추가시켜주기
        else :
            try :
                sentense_wanted[sentense] = round(log(2 + int(recommend_count), 2))
            except :
                sentense_wanted[sentense] = 10

    plt.cla()
    plt.figure(figsize = (5, 8))
    plt.subplot(2, 1, 1)
    plt.title("Desired sentense in " + label)
    plt.pie(sentense_wanted.values(), labels = sentense_wanted.keys(), autopct = '%.2f')

    plt.subplot(2, 1, 2)
    plt.title("Desired life in " + label)
    plt.pie(life_wanted.values(), labels = life_wanted.keys(), autopct = '%.2f')
    plt.savefig(os.path.join(resultPath, label + "_sentenses.png"))

    '''
    try :
            positive_count += round(log(2 + int(comment[2]), 2))
            # print(f"추천수 {comment[2]}개, 로그스케일 적용 시 {round(log(2 + int(comment[2]), 2))}개")
        except ValueError :
            # 추천수가 1,000 개가 넘으면 "1천"등으로 표기되어서 오류가 남. 이 경우에는 그냥 더해주기
            positive_count += 10
    '''