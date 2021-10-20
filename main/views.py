from django.shortcuts import render
from django.http import HttpResponseRedirect, response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from main import models


# 기획전 화면
def index(request):
    return render(request, 'main/index.html')

# 공지사항 화면
def notice(request):
    
    notice_list = models.get_all_notice()

    result = {
        'notice_list' : notice_list
    }

    return render(request, 'main/notice.html' , result)

# FAQ 화면
def faq(request):

    faq_list = models.get_all_faq()

    result = {
        'faq_list' : faq_list
    }

    return render(request, 'main/faq.html', result)

# 1대1 질문 화면
def user_question(request):
    authuser = request.session["authuser"]
    user_no = authuser["user_no"]

    user_question_list = models.get_all_user_question(user_no)

    result = {
        'user_question_list' : user_question_list
    }

    return render(request, 'main/user_question.html', result)

# 1대1 질문 작성 화면
def user_question_write(request):
    return render(request, 'main/user_question_write.html')

# 1대1 질문 등록
def question_register(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/login_form')

    authuser = request.session["authuser"]
    user_no = authuser["user_no"]
    type = request.POST["type"]
    title = request.POST["title"]
    content = request.POST["content"]

    models.question_register(user_no,type,title,content)

    return HttpResponseRedirect('/user_question')

# 개인정보 처리 정책 화면
def personal_infomation_processing_policy(request):
    return render(request, 'main/personal_infomation_processing_policy.html')