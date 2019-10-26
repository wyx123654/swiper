import datetime
from user.models import User

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