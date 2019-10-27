from django.utils.deprecation import MiddlewareMixin
from libs.http import render_json
from common import stat
from user.models import User


class AuthorizeMiddleware(MiddlewareMixin):
    # 登陆验证的中间件

    WHITE_LIST = [
        '/api/user/get_vcode',
        '/api/user/check_vcode',
        '/weibo/wb_auth',
        '/weibo/callback',
    ]

    def process_request(self,request):
    #     url 映射
        # 获取当前用户
        if request.path in self.WHITE_LIST:
            return
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code':stat.LOGIN_REQUIRED,'data':None})
        request.user = User.objects.get(id=uid)

class LogicErrMiddleware(MiddlewareMixin):
    ''' 逻辑异常中间件'''
    def process_exception(self,request,exception):
        if isinstance(exception,stat.LogicErr):
            return render_json(code=exception.code,data=exception.data)



    # def process_view(self):
    # #     view
    # def process_template(self):
    #
    # def process_response(self):
    # #     返回到浏览器
    # def process_exception(self):