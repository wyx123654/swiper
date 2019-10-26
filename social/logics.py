import datetime
from user.models import User
from social.models import Swiped,Friend

def rcmd(user):
    '''推荐可滑动的用户'''
    profile =user.profile
    today = datetime.date.today()

    # 最早出生日期
    earliest_birthday = today -datetime.timedelta(profile.max_dating_age*365)
    # 最晚出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age*365)
    # 筛选出匹配的用户
    users = User.objects.filter(
        sex = profile.dating_sex,
        location = profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    )[:20]
    # ORM 对象关系映射
    # 有很多sql模板，通过模板产生sql语句，然后通过tcp连接，然后链接到mysql
    # TODO：排除滑过的用户
    return users

def like_someone(user,sid):
    '''喜欢某人'''
    Swiped.objects.create(uid = user.id,sid=sid,stype='like')  #添加滑动记录
    # 检查对方是否喜欢过自己,如果喜欢过自己匹配成好友关系
    if Swiped.is_liked(sid,user.id):
        # TODO:如果对方喜欢过自己匹配成好友
        Friend.make_friends(user.id,sid)
        return True
    else:
        return False


