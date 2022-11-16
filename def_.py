import calendar
import numpy as np

months = [9,10,11,12,1,2,3,4,5,6,7,8]
day_month = [calendar.monthrange(2022, month)[1] for month in months] # [30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31]


# 9월부터 다음해 8월까지 day를 나열한 값이 각각 몇번째 중복되는 값인지 나열되어있는 리스트
def ready(idx=1):

    day_all_flatten = []
    for day in day_month:
        for num in range(1, day+1):
            day_all_flatten.append(num)

    day_all_flatten = np.array(day_all_flatten)

    ls = []
    for idx_num, day in enumerate(day_all_flatten):
    # 현재가 9월이라면 네이버 항공권에서 첫번째 28일은 9월 28일이고 두번째 28일은 10월 28이다. 
    # 따라서 몇 번째 값인지를 기준으로 몇 월인지를 파악한다.
    # 현재 day에 해당하는 숫자가 day_all_flatten에서 몇번째 중복되는 값인지 알자
        itr = np.where(day_all_flatten == day)[0].tolist().index(idx_num)
        ls.append(itr)
    
    depart_day_all = day_all_flatten[idx-1:-9] # 출발 일자 리스트
    back_day_all = day_all_flatten[idx+8:] # 도착 일자 리스트

    ls_depart = ls[idx-1:-9] # 몇번째 중복값인지 인덱스
    ls_back = ls[idx+8:] # 몇번째 중복값인지 인덱스
    


    print(len(depart_day_all), len(back_day_all), len(ls_depart), len(ls_back)) # 개수가 모두 일치함을 확인
    return depart_day_all, ls_depart, back_day_all, ls_back