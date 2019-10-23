from django.shortcuts import render
from user import logics
from django.http import JsonResponse
# Create your views here.
# 获取短信验证码
def get_vcode(request):
    # .GET  .POST .COOKIES .session .FILES .META
    phonenum = request.GET.get('phonenum')
#     发送验证码,并且检查是否发送成功
    if logics.send_vcode(phonenum):
        return JsonResponse({'code':0,'data':None})
    else:
        return JsonResponse({'code':1,'data':None})


# 进行短信验证，并且登陆或者注册
def check_code(request):
    pass