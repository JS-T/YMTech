# coding:utf-8

from __future__ import unicode_literals
from django.db import models
from ymtech.models.env import *

# Create your models here.


class CommonCsvDataModel(models.Model):
    class Meta:
        verbose_name = '数据'
        verbose_name_plural = '数据'
    id = models.IntegerField(primary_key=True, editable=False)
    env = models.ForeignKey(CommonEnvDataModel, verbose_name='实验', default=0)
    comments = models.TextField('描述', blank=True)

    index_time = models.FloatField('时间', blank=True, default=0)
    torque = models.FloatField('扭矩', blank=True, default=0)
    speed = models.FloatField('转速', blank=True, default=0)
    pressure = models.FloatField('压力', blank=True, default=0)
    micro_polarity = models.FloatField('油膜厚度', blank=True, default=0)
    dynamic_friction_coefficient = models.FloatField('动摩擦系数', blank=True, default=0)
