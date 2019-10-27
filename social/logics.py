import time
import datetime
from common import keys, stat
from user.models import User
from social.models import Swiped,Friend
from libs.cache import rds
from swiper import cfg

def rcmd(user):
    '''推荐可滑动的用户'''
    profile =user.profile
    today = datetime.date.today()

    # 最早出生日期
    earliest_birthday = today -datetime.timedelta(profile.max_dating_age*365)
    # 最晚出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age*365)
    # 取出滑过的用户的ID
    sid_list = Swiped.objects.filter(uid = user.id).values_list('sid',filat = True)
    # 取出超级喜欢自身，但是没有被自己滑动过的用户的ID

    # 使用orm取
    # who_superlike_me = Swiped.objects.filter(sid=user.id,style='superlike').exclude(uid__in=sid_list).values_list('uid',flat=True)

    # 使用redis取出
    superliked_me_id_list = [int(uid) for uid in rds.zrange(keys.SUPERLIKED_KEY % user.id ,0,19)]
    superliked_me_users = User.objects.filter(id__in = superliked_me_id_list)

    # 筛选出匹配的用户
    other_count =20 - len(superliked_me_users)
    if other_count>0:
        other_users = User.objects.filter(
            sex = profile.dating_sex,
            location = profile.dating_location,
            birthday__gte=earliest_birthday,
            birthday__lte=latest_birthday
        ).exclude(id__in=sid_list)[:20]
        users = superliked_me_users | other_users
        # ORM 对象关系映射
        # 有很多sql模板，通过模板产生sql语句，然后通过tcp连接，然后链接到mysql
    else:
        users = superliked_me_users
    return users

def like_someone(user,sid):
    '''喜欢某人'''
    Swiped.swipe(user.id,sid,'like')  # 添加滑动记录
    # 检查对方是否喜欢过自己,如果喜欢过自己匹配成好友关系
    if Swiped.is_liked(sid,user.id):
        # 如果对方喜欢过自己匹配成好友
        Friend.make_friends(user.id,sid)
        return True
    else:
        return False

def superlike_someone(user,sid):
    '''    自己超级喜欢过对方，则一定会出现在对方的推荐列表里面 '''
    Swiped.swipe(user.id,sid,'superlike')

    rds.sadd(keys.SUPERLIKED_KEY % sid, {user.id:time.time()})   # 把自己的id写入到对方的优先推荐队列


    # 检查对方是否喜欢过自己,如果喜欢过自己匹配成好友关系
    if Swiped.is_liked(sid, user.id):
        Friend.make_friends(user.id, sid)
        # 如果对方超级喜欢过你,把对方从你的超级喜欢列表中删除
        rds.zrem(keys.SUPERLIKED_KEY % user.id,sid)
        return True
    else:
        return False

def dislike_someone(user,sid):
    '''不喜欢某人'''
    Swiped.swipe(user.id,sid,'dislike')   #添加滑动记录
    # 无论对方是否超级喜欢过你，都直接删除掉
    rds.zrem(keys.SUPERLIKED_KEY % user.id ,sid)


def rewind_swipered(user):
    '''反悔一次滑动记录'''

    # 获取今天的反悔次数
    rewind_times = rds.get(keys.REWIND_KEY % user.id,0)
    # 检查今天返回是否达到了反悔上限
    if rewind_times >= cfg.DAILY_REWIND:
        raise stat.RewindLimit
    # 找到最近的一次滑动记录
    latest_swiped = Swiped.objects.filter(uid=user.id).latest('stime')
    # 检查反悔的记录是否是五分钟之内的
    now = datetime.datetime.now()
    if (now - latest_swiped.stime).total_seconds() >= cfg.REWIND_TIMEOUT:
        raise stat.RewindTimeout
    # 检查上一次滑动是否有可能匹配了好友关系
    if latest_swiped.stype in ['like','superlike']:
        # 删除好友关系
        Friend.break_off(user.id,latest_swiped.sid)

        # 如果上一次是超级喜欢 将自身的uid从对方的优先推荐队列里面删除
        if latest_swiped.stype =='superlike':
            rds.zrem(keys.SUPERLIKED_KEY % latest_swiped.sid,user.id)

    # 删除滑动记录
    latest_swiped.delete()
    # 更新当天的滑动词数,同时设置过期时间到下一个凌晨
    next_zero = datetime.datetime(now.year,now.month,now.day)+datetime.timedelta(1)
    remain_seconds = (next_zero - now).total_seconds()
    rds.set(keys.REWIND_KEY % user.id,rewind_times +1,int(remain_seconds))


