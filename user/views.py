from django.shortcuts import render
from django.http import HttpResponseRedirect, response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from user import models



# 회원가입 약관 동의 화면
def sign_agree(request):
    return render(request, 'user/sign_agree.html')


# 회원가입 페이지 보여주기
def sign_form(request):
    if 'authuser' in request.session:
        return HttpResponseRedirect('/')
    return render(request, 'user/sign_form.html')


# 이메일로 중복 체크
def sign_check(request):
    email = request.GET["email"]
    yesorno = models.sign_check(email)

    if yesorno == None:
        tmp_result = "ok"
    else:
        tmp_result = "exist"

    result = {
        'data' : tmp_result
    }

    return JsonResponse(result)


# 회원가입 요청
def sign_func(request):
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    gender = request.POST["gender"]
    agree_personal = request.POST["agree"]
    phone = request.POST["phone"]
    birth = request.POST["birth"]
    image = request.POST["image"]

    models.sign_insert(name, email, password, gender, agree_personal, phone,birth,image)

    return HttpResponseRedirect('/sign_success')


# 회원가입 성공
def sign_success(request):
    return render(request, 'user/sign_success.html')


# 로그인 화면으로
def sign_success_toLogin(request):
    return HttpResponseRedirect('/login_form')


# 로그인 하는 화면
def login_form(request):
    if 'authuser' in request.session:
        return HttpResponseRedirect('/')
    return render(request, 'user/login_form.html')


# 로그인 
def login_func(request):
    email = request.POST["email"]
    password = request.POST["password"]

    result = models.login_findby_email_and_password(email,password)
    if result is None:
        return HttpResponseRedirect('login_form?result=fail')

    request.session["authuser"] = result 

    return HttpResponseRedirect('/')


# 로그아웃
def logout(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    del request.session["authuser"]
    
    return HttpResponseRedirect('/')


# 유저 개인정보수정 화면
def revise_form(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.user_findbyno(authuser["user_no"])

    data = {'data': result}

    return render(request, 'user/revise_form.html',data)


# 수정하기
def revise_func(request):

    authuser = request.session["authuser"]
    user_no = authuser["user_no"]
    password = request.POST["password"]
    phone = request.POST["phone"]

    models.revise_insert(user_no,password,phone)

    return HttpResponseRedirect('info_form')

# 유저 간단 정보, 기타 화면으로 이동할 수 있는 페이지

from datetime import datetime, timedelta
def info_form(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/login_form')

    authuser = request.session["authuser"]
    user_result = models.user_findbyno(authuser["user_no"])

    data = {
        'user_info' : user_result
    }
    return render(request, 'user/info_form.html',data)

# 섭취정보
def info_drug(request):
    if 'authuser' not in request.session:
        return render(request, 'user/first_page.html')

    authuser = request.session["authuser"]

    # 성별 가져오기
    for_sex = models.user_findbyno(authuser["user_no"])

    # 사용자 섭취중인 약 리스트
    yak_result = models.yak_findbyuserno(authuser["user_no"])


    if yak_result == ():
        return render(request, 'user/info_drug_null.html')
    else:
        
        extract_result = models.yak_calculate_vitamin(authuser["user_no"])
        cnt = 0
        extract_result_except_recommend = models.calculate_except_recommend(authuser["user_no"])

        # 커스텀 리스트 가져오기 
        custom_yak_result = models.yak_findbyuserno_custom(authuser["user_no"])

        data = {
            'yak_info' : yak_result,
            'extract_re' : extract_result,
            'for_sex' : for_sex,
            'cnt' : cnt,
            'extract_except_recommend' : extract_result_except_recommend,
            'custom_yak_info' : custom_yak_result
        }

        return render(request, 'user/info_drug.html',data)
    

# 섭취중인 약 삭제
def del_drug(request):
    del_num = request.GET["no"]
    authuser = request.session["authuser"]

    models.del_drug_by_no(authuser["user_no"],del_num)

    return HttpResponseRedirect('/')


# 섭취중인 커스텀 약 삭제
def del_drug_custom(request):
    del_num = request.GET["no"]
    authuser = request.session["authuser"]

    models.del_drug_by_no_custom(authuser["user_no"],del_num)

    return HttpResponseRedirect('/')


# 섭취중,섭취예정,섭취완료 변경
def change_state(request):
    
    state = request.GET["state"]
    authuser = request.session["authuser"]
    name = request.GET["name"]
    custom_noncustom = request.GET["custom_noncustom"]

    if custom_noncustom == 'main':
        models.change_state_model(state,authuser["user_no"],name)
    else:
        models.custom_change_state_model(state,authuser["user_no"],name)

    extract_result = models.yak_calculate_vitamin(authuser["user_no"])
    extract_result_except_recommend = models.calculate_except_recommend(authuser["user_no"])

    result = {
        'extract_re' : extract_result,
        'extract_except_recommend' : extract_result_except_recommend
    }

    return JsonResponse(result)


# 임산부 수유부
def change_woman(request):
    
    state = request.GET["state_woman"]
    authuser = request.session["authuser"]

    extract_result = models.calculate_woman(authuser["user_no"],state)

    result = {
        'extract_re' : extract_result
    }

    return JsonResponse(result)

# 1대1 질문..???
def user_question(request):
    return render(request, 'user/user_question.html')



