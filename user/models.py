from django.db import models
from vip.models import Vip

class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('重庆', '重庆'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('沈阳', '沈阳'),

    )
    phonenum = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birthday = models.DateField(default='1990-1-1', verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=20, choices=LOCATION, verbose_name='常住地')

    vip_id = models.IntegerField(default=1,verbose_name='用户对用的VIP')
    vip_expired = models.DateTimeField(default='2000-1-1',verbose_name='会员过期时间')

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }

    @property
    def profile(self):
        if not hasattr(self,'_profile'):
            self._profile,_ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

class Profile(models.Model):
    # 交友资料
    dating_sex = models.CharField(max_length=8, choices=User.SEX, verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=20, choices=User.LOCATION, verbose_name='目标城市')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=30, verbose_name='最大查找范围')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='只让匹配的人看我相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    def to_dict(self):
        return {
            'id':self.id,
            'dating_sex':self.dating_sex,
            'dating_location':self.dating_location,
            'min_dating_age':self.min_dating_age,
            'max_dating_age':self.max_dating_age,
            'min_distance':self.min_distance,
            'max_distance':self.max_distance,
            'vibration':self.vibration,
            'only_matched':self.only_matched,
            'auto_play':self.auto_play
        }


