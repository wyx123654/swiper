from django.shortcuts import render
from libs.http import render_json


def ger_rcmd_users(request):
    '''获取推荐用户'''
    return render_json()

def like(request):
    '''右滑喜欢'''
    return render_json()
def superlike(request):
    ''''上滑-超级喜欢'''
    return render_json()
def dislike(request):
    '''左滑-不喜欢'''
    return render_json()
def rewind(request):
    '''反悔'''
    return render_json()
def who_liked_me(request):
    '''谁喜欢我'''
    return render_json()
def friend_list(request):
    '''获取好友列表'''
    return render_json()