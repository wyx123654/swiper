import requests
import random
from django.core.cache import cache
from swiper import cfg
from common import keys

def gen_randcode(length:int)->str:
#     产生指定长度的随机码
    chars=[str(random.randint(0,9))for i in range(length)]
    return ''.join(chars)

def send_vcode(phone):
    vcode=gen_randcode(6)
    cache.set(keys.VCODE_KEY % phone,vcode,180)  #验证码添加到缓存中,并且设置过期时间
    sms_args = cfg.YZX_ARGS.copy()
    sms_args['param']=vcode
    sms_args["mobile"]=phone
    response = requests.post(cfg.YZX_API,json=sms_args)
    # 检查最终的返回值
    if response.status_code ==20:
        result = response.json()
        if result['code']=='000000':
            return True
    return False

def get_access_token(code):
    # 获取微博的授权令牌
    args = cfg.WB_ACCESS_TOKEN_ARGS.copy()
    args['code']=code
    response = requests.post(cfg.WB_ACCESS_TOKEN_API,data=args)
    # 检查最终的返回值
    if response.status_code == 20:
        result = response.json()
        access_token = result['access_token']
        wb_uid =result['uid']
        return access_token,wb_uid
    return None,None


def get_user_info(access_token,wb_uid):
    args = cfg.WB_USER_SHOW_ARGS.copy()
    args['access_token']=access_token
    args['uid'] = wb_uid
    response = requests.get(cfg.WB_USER_SHOW_API,params=args)
    # 检查最终的返回值
    if response.status_code == 20:
        result = response.json()
        user_info={
            'phonenum':'WB_%s'% wb_uid,
            'nickname':result['screen_name'],
            'sex':'female' if result['gender']=='f' else 'male',
            'avator':result['avator_hd'],
            'location':result['location'].split(' ')[0],
        }
        return user_info
    return None




