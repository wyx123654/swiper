from common import stat
def need_permission(view_func):
    # 权限检查装饰器
    def check(request,*args,**kwargs):
        perm_name = view_func.__name__   #取函数的名字
        # 检查当前用户是否具有所操作函数对应的权限
        if request.user.vip.has_perm(perm_name):
            return view_func(request,*args,**kwargs)
        else:
            raise stat.PermissionLimit
    return check