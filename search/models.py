
from django.db import models
from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor
from django.http import response

from datetime import datetime, timedelta

# 사진 classification 결과에 대한 정보
def classification_result(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select dosage,unit,extract_name,effects,caution 
            from ingredient_db inner join main_db on main_db.main_no = ingredient_db.main_db_no 
					inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
            where main_db.main_no = %s
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# 텍스트 검색 후 클릭한 해당 약에 대한 정보
def text_search_result(name):
    db = conn()

    cursor = db.cursor(DictCursor)

    

    sql = '''
            select *
            from ingredient_db inner join main_db on main_db.main_no = ingredient_db.main_db_no 
					inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
            where main_db.name = %s
            '''
    cursor.execute(sql, (name,))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# 사진 classification 결과에 대한 주의사항
def caution_main(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select intake_info, prod_caution, brand, name, main_db_no, image, storage_caution, prod_effectiveness
            from caution_db , main_db
            where caution_db.main_db_no = main_db.main_no and main_db.main_no = %s
            '''
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

# 텍스트 검색 후 클릭한 해당 약에 대한 주의사항
def caution_main_text(name):
    db = conn()

    cursor = db.cursor(DictCursor)


    sql = '''
            select intake_info, prod_caution, brand, name, main_db_no, image, storage_caution, prod_effectiveness
            from caution_db , main_db
            where caution_db.main_db_no = main_db.main_no and main_db.name = %s
            '''
    cursor.execute(sql, (name,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

# 이미지 찾아서 가져오기
def find_image(main_db_no):
    db = conn()

    cursor = db.cursor(DictCursor)
    
    sql = '''
            select image
            from main_db
            where main_no = %s
            '''
    cursor.execute(sql, (main_db_no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

# 결과 페이지에서 등록하기 하면 약이 등록
def prod_insert(user_no, main_db_no,date):
    try:
        
        db = conn()

        cursor = db.cursor()

        date_split = date.split('-')
        register_date = datetime(int(date_split[0]),int(date_split[1]),int(date_split[2]))
        now_date = datetime.now()
        date_calculate = (now_date - register_date).days

        if date_calculate < 0:
            state = '섭취예정'
        else:
            state = '섭취중'

        sql = 'insert into user_owned_db values (%s,%s,%s,%s);'
        count = cursor.execute(sql, (user_no, main_db_no, date, state))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

# 함량 단위 리턴 함수 
def extract_unit_return_model(extract_name):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select regular_unit
            from extract_db
            where extract_name = %s
            '''
    cursor.execute(sql, (extract_name,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

# 텍스트로 약 찾기 (약품명), 상세검색 포함
def search_text(name,num,brand,effects,extract,min,max):
    db = conn()

    cursor = db.cursor(DictCursor)
    
    sql = '''
            select *
            from main_db inner join ingredient_db on main_db.main_no = ingredient_db.main_db_no
			             inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
            where main_db.name regexp %s and
                main_db.brand regexp %s and
                main_db.keyword regexp %s
            '''

    limit = 'group by main_db.name having count(*) >= %s limit %s,10'

    if extract != '':
        extract_list = extract.split(',')
        min_list = min.split(',')
        max_list = max.split(',')
        sql = sql + ' and '
        extract_cnt = len(extract_list)
        for i in range(len(extract_list)):
            extract_text = '(extract_db.extract_name like "' + extract_list[i] + '" and '
            dosage_text = 'ingredient_db.dosage between ' + min_list[i] + ' and ' + max_list[i] + ') '
            sql = sql + extract_text + dosage_text
            if i != len(extract_list) - 1:
                sql = sql + ' or '

    else:
        extract_cnt = 0

    sql = sql + limit
    
    cursor.execute(sql, (name,brand,effects,extract_cnt,num))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# 텍스트로 약찾기 개수, 상세검색 포함
def search_text_cnt(name,brand,effects,extract,min,max):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
            select count(DISTINCT main_db.name) as cnt
            from main_db inner join ingredient_db on main_db.main_no = ingredient_db.main_db_no
			             inner join extract_db on ingredient_db.extract_db_no = extract_db.extract_no
            where main_db.name regexp %s and
                main_db.brand regexp %s and
                main_db.keyword regexp %s
            '''

    limit = 'group by main_db.name having count(*) >= %s'
    total_count = '''
                    select count(*) as cnt
                    from (
                '''

    if extract != '':
        extract_list = extract.split(',')
        min_list = min.split(',')
        max_list = max.split(',')
        sql = sql + ' and '
        extract_cnt = len(extract_list)
        for i in range(len(extract_list)):
            extract_text = '(extract_db.extract_name like "' + extract_list[i] + '" and '
            dosage_text = 'ingredient_db.dosage between ' + min_list[i] + ' and ' + max_list[i] + ') '
            sql = sql + extract_text + dosage_text
            if i != len(extract_list) - 1:
                sql = sql + ' or '

    else:
        extract_cnt = 0

    sql = sql + limit

    total_count = total_count + sql + ') as c'
  
    cursor.execute(total_count, (name,brand,effects,extract_cnt))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result





# ########################################################
# # 약 정답 맞추기 뿡뿡
# import os,glob, pathlib
# import numpy as np
# from PIL import Image

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.models import Sequential, load_model, Model
# from keras.layers import LayerNormalization

# import urllib.request

# file_name = os.path.dirname(__file__) + '\\whycannot.h5'
# model = load_model(file_name)

# def tmptmp(img_tt):

#     train_list = ['(한국) 센트룸 멀티구미 40구미',
#     '(한국) 센트룸 멀티구미 80구미',
#     '(한국) 센트룸 멀티비타민 112정 포 맨',
#     '(한국) 센트룸 멀티비타민 112정 포 우먼',
#     '(한국) 센트룸 멀티비타민 125정 포 키즈',
#     '(한국) 센트룸 멀티비타민 50정 포 맨',
#     '(한국) 센트룸 멀티비타민 50정 포 우먼',
#     '(한국) 센트룸 멀티비타민 60정 포 키즈',
#     '(한국) 센트룸 멀티비타민 70정 포 맨',
#     '(한국) 센트룸 멀티비타민 70정 포 우먼',
#     '(한국) 센트룸 실버 멀티비타민 112정 포 맨',
#     '(한국) 센트룸 실버 멀티비타민 112정 포 우먼',
#     '(한국) 센트룸 실버 멀티비타민 50정 포 맨',
#     '(한국) 센트룸 실버 멀티비타민 50정 포 우먼',
#     '(한국) 센트룸 실버 멀티비타민 70정 포 맨',
#     '(한국) 센트룸 실버프로 120정',
#     '(한국) 센트룸 칼슘+D 미니 120정',
#     '(한국) 센트룸 칼슘+D 미니 265정',
#     '(한국) 센트룸 프로 120정',
#     '(해외) centrum multivitamin men 250 tab',
#     '(해외) centrum silver adults 50+ 325 tab',
#     '(해외) centrum silver men 50+ 275',
#     '(해외) centrum women 250 tab',
#     '고려은단 비타민C 1000 120정',
#     '고려은단 비타민C 1000 180정',
#     '고려은단 비타민C 1000 300정',
#     '고려은단 비타민C 1000 480정',
#     '고려은단 비타민C 1000 600정',
#     '고려은단 비타민C 1000 60정',
#     '고려은단 비타민C 1000 이지 180정',
#     '락토핏 생 유산균 골드 50포',
#     '로하비 프리미엄 밀크씨슬 이엑스 120정',
#     '속편한 고려은단 비타민C 1000 120정',
#     '슈퍼비젼 멀티비타민 미네랄 로얄 180정',
#     '애터미헤모힘 20ml 60포',
#     '애터미헤모힘 20ml 6포',
#     '애터미헤모힘 20ml 낱개',
#     '얼라이브 원스데일리 60정',
#     '얼라이브 원스데일리 포 우먼 60정',
#     '얼라이브 원스데일리 포맨 60정',
#     '종근당건강 멀티비타민 포맨 216정',
#     '종근당건강 프로메가 오메가3 60정',
#     '지엔엠 GNM자연의품격 100억유산균 60정',
#     '지엔엠라이프 GNM자연의품격 건강한 간 밀크씨슬 30정',
#     '지엔엠라이프 GNM자연의품격 루테인오메가3 30정',
#     '지엔엠라이프 GNM자연의품격 종합비타민미네랄15 90정',
#     '토날린 블랙짚 익스트림 맥스 우먼 112정',
#     '토날린 블랙짚 익스트림맥스 맨 112정',
#     '튼튼닷컴 루테인 프리미엄 180정',
#     '튼튼닷컴 밀크씨슬 180정']


#     # model = load_model(os.path.join("prec/search/","whycannot.h5"))
#     # model = load_model('https://btp4img.s3.ap-northeast-2.amazonaws.com/H5/B5_50class_epoch100%2Cbatch4%2C380.h5')
    

#     height = model.input_shape[1]
#     width = model.input_shape[2]
    

#     # url = img_tt
    
#     # req = urllib.request.Request(url, headers = {"User-Agent" : "Mozilla/5.0"})
#     # res = urllib.request.urlopen(req)

#     X = []

#     img = Image.open(img_tt)
#     img = img.convert("RGB")
#     img = img.resize((width, height))
#     data = np.asarray(img)
#     X.append(data)

#     X = np.array(X)
#     X = X/255

#     prediction = model.predict(X)


#     pre_ans = prediction.argmax()+1
        

#     return pre_ans

# 커스텀 약 등록
def custom_register_model(user_no,img,name,brand,number,per_day,extract,dosage,date):
    try:
        db = conn()

        cursor = db.cursor()

        date_split = date.split('-')
        register_date = datetime(int(date_split[0]),int(date_split[1]),int(date_split[2]))
        now_date = datetime.now()
        date_calculate = (now_date - register_date).days

        if date_calculate < 0:
            state = '섭취예정'
        else:
            state = '섭취중'

        # user_custom_db 에서 custom_no (커스텀 약 넘버)에서 가장 큰거 가져오기
        sql = '''select max(custom_no) as max_numbering from custom_main_db'''
        cursor.execute(sql, ())
        result = cursor.fetchone()
        # result 에서 가져와서 max_numbering 가져오고 여기서 +1 해서 

        if str(result) == '(None,)':
            max_numbering = 1
        else:
            print(result[0])
            max_numbering = int(result[0]) + 1

        print(max_numbering)

        # 이미지 업로드하고 이미지 url 가져옴
        img_url = s3_upload(img, user_no, max_numbering)

        # custom_main_db 등록
        sql = 'insert into custom_main_db values (null, %s,%s,%s,%s,%s);'
        cursor.execute(sql, (img_url, name,brand,number,per_day))
        # commit
        db.commit()

        # custom_user_owned_db 등록
        sql = 'insert into custom_user_owned_db values (%s,%s,%s,%s);'
        cursor.execute(sql, (user_no, max_numbering, date,state))
        db.commit()

        # custom_ingredient_db 등록
        extract_list = extract.split(',')
        min_list = dosage.split(',')

        for i, j in zip(extract_list,min_list):
            sql = '''select extract_no from extract_db where extract_name = %s'''
            cursor.execute(sql, (i,))
            result = cursor.fetchone()

            sql = 'insert into custom_ingredient_db values (%s, %s, %s)'
            count = cursor.execute(sql, (max_numbering,result[0],j))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

# S3에 사진 업로드하고 해당 사진의 링크 가져오기
import boto3

AWS_ACCESS_KEY_ID = 'AKIAY476GMU573BOUD53'
AWS_SECRET_ACCESS_KEY = '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'

def s3_upload(image_file,user_no,max_numbering):
    # 여기서 max_numbering은 이미 +1이 되어있는 거라서 건드리지 말 것

    s3_client = boto3.client(
		's3',
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	    )
        
    test = str(user_no) + '-' +str(max_numbering) + '.jpg'
    s3_client.upload_fileobj(
        image_file,
        'bitbits3test',
        test,
        ExtraArgs={
            "ContentType": image_file.content_type,
        }
    )

    return_url = 'https://bitbits3test.s3.ap-northeast-2.amazonaws.com/' + test

    return return_url

    print('https://bitbits3test.s3.ap-northeast-2.amazonaws.com/' + test)
    
    
    # s3 = boto3.client('s3') 
    # bucket_name = 'bitbits3test' 
    # nm = 1

    # src = str(image_file)

    # # 첫본째 매개변수 : 로컬에서 올릴 파일이름 # 두번째 매개변수 : S3 버킷 이름 # 세번째 매개변수 : 버킷에 저장될 파일 이름. 
    # s3.upload_file(src, bucket_name, str(nm)+src)
    
    # s3 = boto3.resource('s3')
    # bucket = s3.Bucket(bucket_name)
    # file_list = 

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
        user='tester',
        password='1234',
        host='localhost',
        port=3306,
        db='test',
        charset='utf8')