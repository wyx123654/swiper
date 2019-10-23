import requests
import random
from swiper import cfg

def gen_randcode(length:int)->str:
#     产生指定长度的随机码
    chars=[str(random.randint(0,9))for i in range(length)]
    return ''.join(chars)

def send_vcode(phone):
    vcode=gen_randcode(6)
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