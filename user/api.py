from django.shortcuts import render, redirect
from user import logics
from django.http import JsonResponse
from django.core.cache import cache
from common import keys, stat
from user.models import User
from swiper import cfg


# 获取短信验证码
def get_vcode(request):
    # .GET  .POST .COOKIES .session .FILES .META
    phonenum = request.GET.get('phonenum')
    #     发送验证码,并且检查是否发送成功
    if logics.send_vcode(phonenum):
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


# 进行短信验证，并且登陆或者注册
def check_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cache_vcode = cache.get(keys.VCODE_KEY % phonenum)  # 从缓存取验证码
    if vcode == cache_vcode and vcode and cache_vcode:
        #     取出用户
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果用户不存在直接创建出来
            user = User.objects.create(
                phonenum=phonenum,
                nickname=phonenum
            )
        request.session['uid'] = user.id
        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': stat.INVILD_VCODE, 'data': None})


def wb_auth(request):
    # 用户授权页
    return redirect(cfg.WB_AUTH_URL)


def wb_callback(request):
    # 微博回调过程
    code = request.GET.get('code')
    # 获取授权令牌
    access_token, wb_uid = logics.get_access_token(code)
    if not access_token:
        return JsonResponse({'code': stat.ACCESS_TOKEN_ERR, 'data': None})
    # 获取用户信息
    user_info = logics.get_user_info(access_token, wb_uid)
    if not user_info:
        return JsonResponse({'code': stat.USER_INFO_ERR, 'data': None})
    # 执行登陆或者注册
    try:
        user = User.objects.get(phonenum=user_info['phonenum'])
    except User.DoesNotExist:
        #     如果用户不存在直接创建出来
        user = User.objects.create(**user_info)

    request.session['uid'] = user.id
    return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
