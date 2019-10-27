from django.shortcuts import render
from libs.http import render_json
from social import logics
from social.models import Swiped, Friend
from user.models import User
from vip.logics import need_permission

def ger_rcmd_users(request):
    '''获取推荐用户'''
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(data=result)


def like(request):
    '''右滑喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.user, sid)
    return render_json({'matched': is_matched})


@need_permission
def superlike(request):
    ''''
    上滑-超级喜欢
    '''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.user, sid)
    return render_json({'matched': is_matched})


def dislike(request):
    '''左滑-不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.user, sid)
    return render_json()


@need_permission
def rewind(request):
    '''
    反悔
    1  客户端传来的东西不可信，所有内容都需要验证
    2  接口的参数和返回值保存吝啬原则，不要把无关的东西传回去
    3  服务器能够直接获取的数据，不要由客户端传递
    '''
    logics.rewind_swipered(request.user)

    return render_json()


@need_permission
def show_liked_me(request):
    '''谁喜欢我'''
    user_id_list = Swiped.who_liked_me(request.user.id)
    users = User.objects.filter(id__in=user_id_list)
    result = [user.to_dict() for user in users]
    return render_json(result)


def friend_list(request):
    '''获取好友列表'''
    friend_id_list = Friend.friend_ids(request.user.id)
    users = User.objects.filter(id__in=friend_id_list)
    result = [user.to_dict() for user in users]
    return render_json()
