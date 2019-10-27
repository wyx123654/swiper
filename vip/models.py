from django.db import models

class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=10,unique=True,verbose_name='会员名称')
    level = models.IntegerField(default=0,verbose_name='会员等级')
    pirce = models.FloatField(default=0.0,verbose_name='当前会员对应的价格')
    days = models.IntegerField(default=0,verbose_name='购买的天数')

    def has_perm(self,perm_name):
#     检查当前的vip是否具有某个权限
        perm = Permission.objects.filter(name = perm_name).only('id')
        return VipPermRelation.objects.filter(vip_id = self.id,perm_id=perm.id).exist()

class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=20,unique=True,verbose_name='权限名称')
    desc = models.TextField(default='',verbose_name='权限的描述')

class VipPermRelation(models.Model):
    vip_id = models.IntegerField(verbose_name='会员的id')
    perm_id = models.IntegerField(verbose_name='权限的id')
