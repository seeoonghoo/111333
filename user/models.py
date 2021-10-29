
from django.db import models
from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor


# info_form에 있는 유저 정보 리턴하기 위한 함수
def user_findbyno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''select *,FLOOR((CAST(REPLACE(CURRENT_DATE,'-','') AS UNSIGNED) - CAST(REPLACE(birth,'-','') AS UNSIGNED)) / 10000) as real_age
     from user_info_db 
     where user_no = %s'''
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


# 이메일 중복체크
def sign_check(email):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select user_no, email from user_info_db where email = %s'
    cursor.execute(sql, (email,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


# 회원가입
def sign_insert(name, email, password, gender, agree, phone,birth,image):
    try:
        db = conn()

        cursor = db.cursor()

        sql = 'insert into user_info_db values(null,%s,%s,%s,%s,now(),%s,%s,%s,%s)'
        count = cursor.execute(sql, (name, password, gender, email, agree, phone,birth,image))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 로그인 할 때 사용
def login_findby_email_and_password(email, password):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        sql = 'select user_no, user_name from user_info_db where email=%s and passwd = %s'
        cursor.execute(sql, (email, password))

        result = cursor.fetchone()

        cursor.close()
        db.close()
        
        return result

    except OperationalError as e:
        print(f'error: {e}')


# 유저 개인 정보 수정
def revise_insert(no,password,phone):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        sql = 'update user_info_db set passwd=%s, phone=%s where user_no = %s'
        count = cursor.execute(sql, (password,phone,no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 사용자별 약 정보 리턴하기 위한 함수
# 사용자의 no를 기준으로 찾아서 리턴
def yak_findbyuserno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select main_no, 
                    name, 
                    image, 
                    date_format(start_date, "%%Y-%%m-%%d") as start_date,
                    number,
                    number - DATEDIFF(now(), start_date) as left_cnt,
                    state
            from main_db join user_owned_db
            where user_info_db_no = %s and main_db.main_no = user_owned_db.main_db_no
            group by main_no
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    for i in result:
        if i['left_cnt'] <= 0:
            change_state_model('섭취완료',no,i['main_no'])

    sql = '''
            select main_no, 
                    name, 
                    image, 
                    date_format(start_date, "%%Y-%%m-%%d") as start_date,
                    number,
                    number - DATEDIFF(now(), start_date) as left_cnt,
                    state
            from main_db join user_owned_db
            where user_info_db_no = %s and main_db.main_no = user_owned_db.main_db_no
            group by main_no
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    for i in result:
        if i['left_cnt'] <= 0:
            i['minus'] = 'minus'
        if i['number'] < i['left_cnt']:
            i['minus'] = 'exceed'

    cursor.close()
    db.close()

    return result


# 사용자별 약 삭제
def del_drug_by_no(user_no, main_no):
    try:
        db = conn()

        cursor = db.cursor()

        sql = '''
            delete from user_owned_db where user_info_db_no = %s and main_db_no = %s;'''
        count = cursor.execute(sql, (user_no,main_no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 커스텀약찾기
def yak_findbyuserno_custom(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select *,
                    date_format(custom_start_date, "%%Y-%%m-%%d") as start_date,
                    custom_number - DATEDIFF(now(), custom_start_date) as left_cnt
            from custom_main_db join custom_user_owned_db
            where custom_user_info_db_no = %s and custom_main_db.custom_no = custom_user_owned_db.custom_main_db_no
            group by custom_no
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    for i in result:
        if i['left_cnt'] <= 0:
            change_state_model('섭취완료',no,i['main_no'])


    sql = '''
            select *,
                    date_format(custom_start_date, "%%Y-%%m-%%d") as start_date,
                    custom_number - DATEDIFF(now(), custom_start_date) as left_cnt
            from custom_main_db join custom_user_owned_db
            where custom_user_info_db_no = %s and custom_main_db.custom_no = custom_user_owned_db.custom_main_db_no
            group by custom_no
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    for i in result:
        if i['left_cnt'] <= 0:
            i['minus'] = 'minus'
        if i['custom_number'] < i['left_cnt']:
            i['minus'] = 'exceed'

    cursor.close()
    db.close()

    return result


# 커스텀약삭제, 메인, 오운드, extract 다 삭제해야함
def del_drug_by_no_custom(user_no, main_no):
    try:
        db = conn()

        cursor = db.cursor()

        # custom_user_info_db_no 삭제
        sql = '''
            delete from custom_user_owned_db where custom_user_info_db_no = %s and custom_main_db_no = %s;'''
        cursor.execute(sql, (user_no,main_no))

        # custom_ingredient_db 삭제
        sql = '''
            delete from custom_ingredient_db where custom_main_db_no = %s;'''
        count = cursor.execute(sql, (main_no,))

        # custom_main_db 삭제하지 않는 이유
        # 이거 분석해서 사람들이 많이 찾는 브랜드나 기타 등등 파악 위해

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 사용자별 섭취량
def yak_calculate_vitamin(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    # SQL 실행
    sql = 'select *, DATEDIFF(now(), birth) as date_cal from user_info_db where user_no = %s'
    cursor.execute(sql, (no,))

    # 결과 받아오기
    result = cursor.fetchone()

    if result['sex'] == '남성':
        real_sex = 'M'
    else:
        real_sex = 'F'

    if result['date_cal'] <= 183:
        age_condition = 'a'
    elif result['date_cal'] > 183 and result['date_cal'] <= 365:
        age_condition = 'b'
    elif result['date_cal'] > 365 and result['date_cal'] <= 731:
        age_condition = 'c'
    elif result['date_cal'] > 731 and result['date_cal'] <= 1826:
        age_condition = 'd'
    elif result['date_cal'] > 1826 and result['date_cal'] <= 2922:
        age_condition = 'e'
    elif result['date_cal'] > 2922 and result['date_cal'] <= 4018:
        age_condition = 'f'
    elif result['date_cal'] > 4018 and result['date_cal'] <= 5114:
        age_condition = 'g'
    elif result['date_cal'] > 5114 and result['date_cal'] <= 6575:
        age_condition = 'h'
    elif result['date_cal'] > 6575 and result['date_cal'] <= 10592:
        age_condition = 'i'
    elif result['date_cal'] > 10592 and result['date_cal'] <= 17897:
        age_condition = 'j'
    elif result['date_cal'] > 17897 and result['date_cal'] <= 23376:
        age_condition = 'k'
    elif result['date_cal'] > 23376 and result['date_cal'] <= 27029:
        age_condition = 'l'
    elif result['date_cal'] > 27029:
        age_condition = 'm'

    # 현재 먹고 있는 약들 
    sql = '''
            select extract_name, round(sum(b),2) as b 
            from
            (select extract_name, round(sum(custom_dosage),2) as b
                        from custom_ingredient_db inner join extract_db on custom_ingredient_db.extract_db_extract_no = extract_db.extract_no
                        where custom_main_db_no in(
                                            select custom_main_db_no
                                            from custom_user_owned_db
                                            where custom_user_info_db_no = %s and custom_state = '섭취중')
                        group by extract_name
            union 
            select extract_name, round(sum(dosage),2) as b
                        from ingredient_db inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
                        where main_db_no in(
                                            select main_db_no
                                            from user_owned_db
                                            where user_info_db_no = %s and state = '섭취중')
						group by extract_name) S
            group by extract_name
            '''

    cursor.execute(sql, (no,no))

    result_false = cursor.fetchall()

    # 모든 성분명
    sql = '''
            select extract_name, dosage_limit, regular_unit, overdose
            from extract_db inner join recommend_db on extract_db.extract_no = recommend_db.extract_db_extract_no
            where age_condition = %s
                and sex = %s
            order by extract_name
            '''

    cursor.execute(sql, (age_condition,real_sex))

    result = cursor.fetchall()


    for i in result:
        if result_false != ():
            
            for j in result_false:
                if i['extract_name'] == j['extract_name']:
                    i['b'] = j['b']
                    break
                else:
                    i['b'] = 0
        else:
            i['b'] = 0 

    cursor.close()
    db.close()

    for i in result:
        if i['b'] < i['dosage_limit'] * 0.3:
            i['color'] = 'yellow'
        elif i['b'] >= i['dosage_limit'] * 0.3 and i['b'] < i['dosage_limit'] * 0.7:
            i['color'] = 'blue'
        else:
            i['color'] = 'green'
        tmp = i['b'] / i['dosage_limit']
        
        if i['overdose'] != 0 and i['b'] > i['overdose']:
            tmp = i['b'] / i['overdose']
            i['color'] = 'dead'

        i['percent'] = int(round(tmp,2) * 100)

    return result


# 사용자별 섭취량에서 권장량 없는 애들
def calculate_except_recommend(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select *, DATEDIFF(now(), birth) as date_cal from user_info_db where user_no = %s'
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    if result['sex'] == '남성':
        real_sex = 'M'
    else:
        real_sex = 'F'

    if result['date_cal'] <= 183:
        age_condition = 'a'
    elif result['date_cal'] > 183 and result['date_cal'] <= 365:
        age_condition = 'b'
    elif result['date_cal'] > 365 and result['date_cal'] <= 731:
        age_condition = 'c'
    elif result['date_cal'] > 731 and result['date_cal'] <= 1826:
        age_condition = 'd'
    elif result['date_cal'] > 1826 and result['date_cal'] <= 2922:
        age_condition = 'e'
    elif result['date_cal'] > 2922 and result['date_cal'] <= 4018:
        age_condition = 'f'
    elif result['date_cal'] > 4018 and result['date_cal'] <= 5114:
        age_condition = 'g'
    elif result['date_cal'] > 5114 and result['date_cal'] <= 6575:
        age_condition = 'h'
    elif result['date_cal'] > 6575 and result['date_cal'] <= 10592:
        age_condition = 'i'
    elif result['date_cal'] > 10592 and result['date_cal'] <= 17897:
        age_condition = 'j'
    elif result['date_cal'] > 17897 and result['date_cal'] <= 23376:
        age_condition = 'k'
    elif result['date_cal'] > 23376 and result['date_cal'] <= 27029:
        age_condition = 'l'
    elif result['date_cal'] > 27029:
        age_condition = 'm'

    sql = '''
            select extract_name, regular_unit,round(sum(b),2) as b 
            from
            (select extract_name, regular_unit,round(sum(dosage),2) as b
            from ingredient_db inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
            where extract_db.extract_no not in (
                                                select extract_db_extract_no
                                                from recommend_db
                                                where age_condition=%s
                                                    and sex = %s) and
                ingredient_db.main_db_no in(
                                            select main_db_no
                                            from user_owned_db
                                            where user_info_db_no = %s and state = '섭취중')
                group by extract_db_no
            union
            select extract_name, regular_unit,round(sum(custom_dosage),2) as b
            from custom_ingredient_db inner join extract_db on custom_ingredient_db.extract_db_extract_no = extract_db.extract_no
            where extract_db.extract_no not in (
                                                select extract_db_extract_no
                                                from recommend_db
                                                where age_condition=%s
                                                    and sex = %s) and
                custom_ingredient_db.custom_main_db_no in(
                                            select custom_main_db_no
                                            from custom_user_owned_db
                                            where custom_user_info_db_no = %s and custom_state = '섭취중')
                group by extract_name) S
            group by extract_name
            order by extract_name'''



    cursor.execute(sql, (age_condition,real_sex,no,age_condition,real_sex,no))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result


# state 변경해주기
def change_state_model(state,user_no,name):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        sql = '''update user_owned_db 
                set state = %s 
                where user_info_db_no = %s 
                    and main_db_no = %s'''
        count = cursor.execute(sql, (state,user_no,name))

        db.commit()
    
        cursor.close()
        db.close()
        
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 커스텀 state 변경해주기
def custom_change_state_model(state,user_no,name):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        sql = '''update custom_user_owned_db 
                set custom_state = %s 
                where custom_user_info_db_no = %s and 
                custom_main_db_no = %s'''
        count = cursor.execute(sql, (state,user_no,name))

        db.commit()
    
        cursor.close()
        db.close()
        
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


# 임산부 수유부
def calculate_woman(no,state):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select *, DATEDIFF(now(), birth) as date_cal from user_info_db where user_no = %s'
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    if result['sex'] == '남성':
        real_sex = 'M'
    else:
        real_sex = 'F'

    if result['date_cal'] <= 183:
        age_condition = 'a'
    elif result['date_cal'] > 183 and result['date_cal'] <= 365:
        age_condition = 'b'
    elif result['date_cal'] > 365 and result['date_cal'] <= 731:
        age_condition = 'c'
    elif result['date_cal'] > 731 and result['date_cal'] <= 1826:
        age_condition = 'd'
    elif result['date_cal'] > 1826 and result['date_cal'] <= 2922:
        age_condition = 'e'
    elif result['date_cal'] > 2922 and result['date_cal'] <= 4018:
        age_condition = 'f'
    elif result['date_cal'] > 4018 and result['date_cal'] <= 5114:
        age_condition = 'g'
    elif result['date_cal'] > 5114 and result['date_cal'] <= 6575:
        age_condition = 'h'
    elif result['date_cal'] > 6575 and result['date_cal'] <= 10592:
        age_condition = 'i'
    elif result['date_cal'] > 10592 and result['date_cal'] <= 17897:
        age_condition = 'j'
    elif result['date_cal'] > 17897 and result['date_cal'] <= 23376:
        age_condition = 'k'
    elif result['date_cal'] > 23376 and result['date_cal'] <= 27029:
        age_condition = 'l'
    elif result['date_cal'] > 27029:
        age_condition = 'm'

    sql = '''
            select extract_name, round(sum(b),2) as b 
            from
            (select extract_name, round(sum(custom_dosage),2) as b
                        from custom_ingredient_db inner join extract_db on custom_ingredient_db.extract_db_extract_no = extract_db.extract_no
                        where custom_main_db_no in(
                                            select custom_main_db_no
                                            from custom_user_owned_db
                                            where custom_user_info_db_no = %s and custom_state = '섭취중')
                        group by extract_name
            union 
            select extract_name, round(sum(dosage),2) as b
                        from ingredient_db inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
                        where main_db_no in(
                                            select main_db_no
                                            from user_owned_db
                                            where user_info_db_no = %s and state = '섭취중')
						group by extract_name) S
            group by extract_name
            '''

    cursor.execute(sql, (no,no))

    result_false = cursor.fetchall()

    # 모든 성분명
    sql = '''
            select extract_name, dosage_limit, regular_unit, overdose
            from extract_db inner join recommend_db on extract_db.extract_no = recommend_db.extract_db_extract_no
            where age_condition = %s
                and sex = %s
            order by extract_name
            '''

    cursor.execute(sql, (age_condition,real_sex))

    result_default = cursor.fetchall()


    for i in result_default:
        if result_false != ():
            
            for j in result_false:
                if i['extract_name'] == j['extract_name']:
                    i['b'] = j['b']
                    break
                else:
                    i['b'] = 0
        else:
            i['b'] = 0 

    # 아래는 임산부 수유부 계산하기 위해 얘네 limit 가져오는 용도

    real_sex = 'F'

    if state == '임산부':
        db_state = 'yy'
    else:
        db_state = 'zz'


    sql = '''
            select extract_name, round(sum(b),2) as b 
            from
            (select extract_name, round(sum(custom_dosage),2) as b
                        from custom_ingredient_db inner join extract_db on custom_ingredient_db.extract_db_extract_no = extract_db.extract_no
                        where custom_main_db_no in(
                                            select custom_main_db_no
                                            from custom_user_owned_db
                                            where custom_user_info_db_no = %s and custom_state = '섭취중')
                        group by extract_name
            union 
            select extract_name, round(sum(dosage),2) as b
                        from ingredient_db inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
                        where main_db_no in(
                                            select main_db_no
                                            from user_owned_db
                                            where user_info_db_no = %s and state = '섭취중')
						group by extract_name) S
            group by extract_name
            '''

    cursor.execute(sql, (no,no))

    result_false = cursor.fetchall()

    # 모든 성분명
    sql = '''
            select extract_name, dosage_limit, regular_unit, overdose
            from extract_db inner join recommend_db on extract_db.extract_no = recommend_db.extract_db_extract_no
            where age_condition = %s
                and sex = %s
            order by extract_name
            '''

    cursor.execute(sql, (db_state,real_sex))

    result_woman = cursor.fetchall()


    for i in result_woman:
        if result_false != ():
            
            for j in result_false:
                if i['extract_name'] == j['extract_name']:
                    i['b'] = j['b']
                    break
                else:
                    i['b'] = 0
        else:
            i['b'] = 0 

            

    for i,g in zip(result_default,result_woman):
        i['dosage_limit'] = float(i['dosage_limit']) + float(g['dosage_limit'])
        i['dosage_limit'] = float(i['dosage_limit'])

    for i in result_default:
        if i['b'] < i['dosage_limit'] * 0.3:
            i['color'] = 'yellow'
        elif i['b'] >= i['dosage_limit'] * 0.3 and i['b'] < i['dosage_limit'] * 0.7:
            i['color'] = 'blue'
        else:
            i['color'] = 'green'
        tmp = i['b'] / i['dosage_limit']

        if i['overdose'] != 0 and i['b'] > i['overdose']:
            tmp = i['b'] / i['overdose']
            i['color'] = 'dead'

        i['percent'] = int(round(tmp,2) * 100)

    return result_default


# def conn():
#     return connect(
#         db='test',
#         user= 'btpadmin',
#         password= '1q2w##3e4r',
#         host= 'btp4mysql.cqzmsvxkugz2.ap-northeast-2.rds.amazonaws.com',
#         port=3306,
#         charset='utf8')

def conn():
    return connect(
        user='root',
        password='apple',
        host='localhost',
        port=3306,
        db='test',
        charset='utf8')