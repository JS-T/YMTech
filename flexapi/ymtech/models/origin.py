# coding:utf-8

from __future__ import unicode_literals
from django.db import models

# Create your models here.


class CommonOriginModel(models.Model):
    class Meta:
        verbose_name = '来源'
        verbose_name_plural = '来源'
    id = models.IntegerField(primary_key=True, editable=False)
    host = models.GenericIPAddressField(
        '地址',
        max_length=255,
        unique=True
    )
    name = models.CharField(
        '名称',
        max_length=255,
        unique=True
    )
    power = models.IntegerField('优先级')
    enabled = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    modified_at = models.DateTimeField('修改时间', auto_now=True)
    secret = models.CharField('密钥', max_length=32, default='')
    comments = models.TextField('描述', blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def status_origin():
        all_origins = CommonOriginModel.objects.filter(enabled=True).order_by('-id')
        tmp_arr = []
        for that_origin in all_origins:
            tmp_arr.append({
                'host': that_origin.host,
                'name': that_origin.name,
                'power': that_origin.power,
                'id': that_origin.id
            })
        return tmp_arr
