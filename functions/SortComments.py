import sys
import os
sys.path.append(os.path.dirname(__file__))
from header import *

# 판결에 관련된 내용들이 많이 포함될 수 있도록 키워드 사용
filters = ["판사", "징역", "판결", "검사", "형량", "재판장", "감형", ]

# 라벨 내의 댓글들을 필터링하여 datas 폴더 내에 _filtered로 저장
def sortComments(label = today) :
    labelPath = os.path.join(dataPath, label)
    fileList = os.listdir(labelPath)

    # 모든 파일 내의 댓글에 대해서 필터링을 수행
    for fileName in fileList :
        # print("파일명 : " + fileName)
        # 필터링된 파일 저장할 폴더 지정
        savePath = os.path.join(dataPath, label + "_filtered")    
        if (not os.path.isdir(savePath)) :
            os.mkdir(savePath)
        
        comments = pd.read_csv(os.path.join(labelPath, fileName), encoding = 'utf-8').to_numpy()
        # print("댓글 수 : " + str(len(comments)))
        comments_save = []

        # 각 댓글 내에 필터에 있는 단어가 잘 들어있는지 검사
        for each in comments :
            try :
                print("댓글 내용 :", each[1])
                # 너무 짧은 댓글도 적절하게 판단이 불가능한 듯. 최소 10자 이상 적었을 경우에만 저장하자
                if (len(each[1]) < 15) :
                    print("15이하")
                    continue
                for word in filters :
                    if word in each[1] :
                        # print(word, "포함되어있음")
                        comments_save.append(each)
                        break
                    else :
                        continue
            except Exception as E:
                print("Error :", E)
                continue
        # 그래도 댓글이 10개는 되어야 저장. 너무 적으면 적절한 의견을 제시했다고 보기 어려우므로.
        if len(comments_save) >= 10 :
            pd.DataFrame(comments_save, columns = ["작성자", "내용", "추천수"]).to_csv(os.path.join(savePath, fileName), index = False)