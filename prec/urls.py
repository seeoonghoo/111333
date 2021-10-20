"""prec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
import main.views as mainviews
import search.views as searchviews
import user.views as userviews
from django.urls import path

# 이미지 업로드용
from django.conf.urls.static import static
from django.conf import settings


# 기능은 마지막에 / 없이
urlpatterns = [
    path('', userviews.info_drug),

    path('exhibitions/', mainviews.index),
    path('notice/', mainviews.notice),
    path('faq/', mainviews.faq),
    path('user_question/', mainviews.user_question),
    path('user_question_write/', mainviews.user_question_write),
    path('question_register', mainviews.question_register),
    path('personal_infomation_processing_policy/', mainviews.personal_infomation_processing_policy),

    path('output/', searchviews.output),
    path('output_text/', searchviews.output_text),
    path('prod_register', searchviews.prod_register),
    path('output_list_form/', searchviews.output_list_form),
    path('camera/', searchviews.camera),
    path('classification', searchviews.classification),
    path('txt_plus_list', searchviews.txt_plus_list),
    path('user_custom/', searchviews.user_custom),
    path('extract_unit_return', searchviews.extract_unit_return),
    path('custom_register', searchviews.custom_register),

    path('sign_agree/', userviews.sign_agree),
    path('sign_form/', userviews.sign_form),
    path('sign_check', userviews.sign_check),
    path('sign_func', userviews.sign_func),
    path('sign_success/', userviews.sign_success),
    path('sign_success_toLogin', userviews.sign_success_toLogin),
    path('change_state', userviews.change_state),
    path('change_woman', userviews.change_woman),
    path('user_question/', userviews.user_question),
    
    path('login_form/', userviews.login_form),
    path('login_func', userviews.login_func),
    path('logout', userviews.logout),
    
    path('revise_form/', userviews.revise_form),
    path('revise_func', userviews.revise_func),

    path('info_form/', userviews.info_form),
    # path('info_drug/', userviews.info_drug),
    path('del_drug', userviews.del_drug),
    path('del_drug_custom', userviews.del_drug_custom),
    

    path('admin/', admin.site.urls)
]

# 이미지 업로드
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)