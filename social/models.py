from django.db import models
from django.db.models import Q
# Create your models here.
# from common.stat import LogicErr,SwipeRepeatErr
import stat

class Swiped(models.Model):
    '''滑动记录'''
    STYPE=(
        ('like','喜欢'),
        ('superlike','超级喜欢'),
        ('dislike','不喜欢')
    )
    uid = models.IntegerField(verbose_name='滑动者的ID')
    sid = models.IntegerField(verbose_name='被滑动者的ID')
    stype = models.CharField(max_length=10,choices=STYPE,verbose_name='滑动的类型')
    stime = models.DateTimeField(auto_now_add=True,verbose_name='滑动时间')

    @classmethod
    def is_liked(clsc,uid,sid):
        '''是否喜欢过某人'''
        condition =Q(stype = 'like')|Q(stype='superlike')
        return  clsc.objects.filter(uid = uid,sid=sid,stype=condition).exists()

    @classmethod
    def swipe(cls,uid,sid,stype):
        '''执行一次滑动'''
        # 检查stype是否正确
        if stype not in ['like','superlike','dislike']:
#             返回一个滑动类型错误
            raise stat.SwipeTypeErr
#         检查是否已经滑动过当前用户
        if cls.objects.filter(uid = uid,sid = sid).exist():
        #      返回一个重复滑动错误
            raise stat.SwipeRepeatErr
        return  cls.objects.create(uid=uid,sid=sid,stype=stype)
    @classmethod
    def who_liked_me(cls,uid):
        return cls.objects.filter(sid = uid,stype__in=['like','superlike']).values_list('uid',flat=True)


# 实例方法 所有普通的方法
# 类方法   @classmethod  方法第一个参数是cls
# 静态方法 @staticmethod


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(clsc,uid,sid):
        '''创建好友关系'''
        uid1,uid2 = (sid,uid) if uid>sid else (uid,sid)
        clsc.objects.geo_or_create(uid1=uid1,uid2=uid2)

    @classmethod
    def friend_ids(cls,uid):
        '''查询所有好友的 ID'''
        condition = Q(uid1 = uid)| Q(uid2 = uid)
        friend_relations=cls.objects.filter(condition)
        uid_list = []
        for relation in friend_relations:
            friend_id = relation.uid2 if relation.uid1 ==uid else relation.uid1
            uid_list.append(friend_id)
        return uid_list




