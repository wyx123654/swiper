from django.db import models
from django.db.models import Q
# Create your models here.
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
        clsc.objects.create(uid1=uid1,uid2=uid2)


