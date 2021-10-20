from django.shortcuts import render
from django.http import HttpResponseRedirect, response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from search import models

# 이미지 classification
def classification(request):
    classification_img= request.FILES.get("bull")

    classification_name = models.tmptmp(classification_img)

    return HttpResponseRedirect('/output?no=%s' % classification_name)

# 이미지 classification 결과 화면
def output(request):
    classification = request.GET["no"]

    good_result = models.classification_result(classification)
    soso_result = models.caution_main(classification)

    data = {
        'ext_result' : good_result,
        'cau_result' : soso_result
    }

    return render(request, 'search/output.html', data)

# 텍스트 검색 결과 리스트에서 해당 약 클릭시 정보 나오는 화면
def output_text(request):
    classification = request.GET["name"]
    good_result = models.text_search_result(classification)
    soso_result = models.caution_main_text(classification)

    data = {
        'ext_result' : good_result,
        'cau_result' : soso_result
    }
    
    return render(request, 'search/output_text.html', data)

# 사용자가 커스텀 약 등록하는 화면
def user_custom(request):

    return render(request, 'search/user_custom.html')

# 약 결과 화면에서 사용자가 등록
def prod_register(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/login_form')

    authuser = request.session["authuser"]
    user_no = authuser["user_no"]
    db_no = request.POST["db_no"]
    date = request.POST["date"]

    models.prod_insert(user_no,db_no,date)

    return HttpResponseRedirect('/')

# 검색 화면
def camera(request):
    return render(request, 'search/camera.html')

# 텍스트 결과 리스트 처음 화면
def output_list_form(request):
    name = request.GET["name"]
    brand = request.GET["brand"]
    effects = request.GET["effects"]
    extract = request.GET["extract"]
    min = request.GET["min"]
    max = request.GET["max"]
   
    result = models.search_text(name,0,brand,effects,extract,min,max)
    txt_result_cnt = models.search_text_cnt(name,brand,effects,extract,min,max)

    for_down = {'name':name, 'brand':brand, 'effects' : effects, 'extract' : extract, 'min' : min, 'max' : max}

    print(type(for_down))

    data  ={
        'text_result' : result,
        "name" : name,
        'txt_cnt' : txt_result_cnt,
        "for_down" : for_down
    }
    
    return render(request, 'search/output_list_form.html',data)

# 아래로 스크롤시 추가적으로 결과 리스트 추가
def txt_plus_list(request):
    name = request.GET["name"]
    brand = request.GET["brand"]
    effects = request.GET["effects"]
    extract = request.GET["extract"]
    min = request.GET["min"]
    max = request.GET["max"]
    num = int(request.GET["num"])

    txt_result = models.search_text(name,num,brand,effects,extract,min,max)
    
    data  ={
        'txt_result' : txt_result
    }

    return JsonResponse(data)


# 정규 함량 나오게 해서 상세 검색 성분에서 사용
def extract_unit_return(request):
    extract_name = request.GET["extract_name"]

    unit = models.extract_unit_return_model(extract_name)

    data  ={
        'unit' : unit
    }

    return JsonResponse(data)

# 사용자가 커스텀으로 작성한 약 등록하기
def custom_register(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/login_form')

    authuser = request.session["authuser"]
    user_no = authuser["user_no"]
    name = request.POST["name"]
    brand = request.POST["brand"]
    number = request.POST["number"]
    per_day = request.POST["per_day"]
    extract = request.POST["extract"]
    dosage = request.POST["dosage"]
    date = request.POST["date"]
    img= request.FILES.get("bull")

    models.custom_register_model(user_no,img,name,brand,number,per_day,extract,dosage,date)

    return HttpResponseRedirect('/')

