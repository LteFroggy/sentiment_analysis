
def 착한댓글판별기(text) :
    test = np.array(text).reshape(1, )
    result = lr.predict(tfidf.transform(test).toarray()).item()
    return True if result == 1 else False

result = 착한댓글판별기("게임 잘하는 배민 존나 고마운분 아기 다람쥐 최인석")
if result :
    print("부정적이지 않은 댓글입니다")
else :
    print("부정적 댓글입니다")