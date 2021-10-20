from django.db import models
from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor

# 공지사항 가져오기
def get_all_notice():
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''select *,
                    date_format(notice_date, "%%Y-%%m-%%d") as real_notice_date
            from admin_notice
            order by notice_no desc'''
    cursor.execute(sql, ())

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# FAQ 가져오기
def get_all_faq():
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''select *
            from admin_faq
            order by faq_no desc'''
    cursor.execute(sql, ())

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# 현재 로그인한 유저의 1대1 질문 가져오기
def get_all_user_question(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''select *,date_format(question_date, "%%Y-%%m-%%d") as real_question_date
            from user_question
            where user_info_db_user_no = %s
            order by question_no desc'''
    cursor.execute(sql, (no,))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

# 현재 로그인한 유저의 1대1 질문 등록
def question_register(user_no,type,title,content):
    try:
        db = conn()

        cursor = db.cursor()

        sql = 'insert into user_question values(%s, null, %s, %s , %s, now(),"" )'
        count = cursor.execute(sql, (user_no, title,content,type))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def conn():
    return connect(
        user='tester',
        password='1234',
        host='localhost',
        port=3306,
        db='test',
        charset='utf8')