# coding:utf-8

from __future__ import unicode_literals
from django.db import models
from ymtech.models.origin import *

# Create your models here.


class CommonEnvDataModel(models.Model):
    class Meta:
        verbose_name = '实验'
        verbose_name_plural = '实验'
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(
        '实验编号',
        max_length=255,
        unique=True
    )
    origin = models.ForeignKey(CommonOriginModel, verbose_name='来源', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    modified_at = models.DateTimeField('修改时间', auto_now=True)
    comments = models.TextField('描述', blank=True)

    initial_speed = models.FloatField('初始转速', blank=True, default=0)
    setting_pressure = models.FloatField('设定压力', blank=True, default=0)
    rotary_inertia = models.FloatField('转动惯量', blank=True, default=0)
    sides_count = models.FloatField('摩擦片面数', blank=True, default=0)

    temperature = models.FloatField('温度', blank=True, default=0)
    inner_diameter = models.FloatField('摩擦片内径', blank=True, default=0)
    outer_diameter = models.FloatField('摩擦片外径', blank=True, default=0)
    plate_thickness = models.FloatField('摩擦片厚度', blank=True, default=0)
    oil_viscosity = models.FloatField('润滑油粘度', blank=True, default=0)
    initial_micro_polarity = models.FloatField('初始油膜厚度', blank=True, default=0)
    surface_roughness = models.FloatField('摩擦材表面粗糙度', blank=True, default=0)
    rough_density = models.FloatField('粗糙密度', blank=True, default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def status_env(that_origin):
        all_envs = CommonEnvDataModel.objects.filter(origin=that_origin).order_by('-id')
        tmp_arr = []
        for that_env in all_envs:
            tmp_arr.append({
                'id': that_env.id,
                'name': that_env.name,
                'constant': {
                    'initial_speed': that_env.initial_speed,
                    'setting_pressure': that_env.setting_pressure,
                    'rotary_inertia': that_env.rotary_inertia,
                    'sides_count': that_env.sides_count,
                    'temperature': that_env.temperature,
                    'inner_diameter': that_env.inner_diameter,
                    'outer_diameter': that_env.outer_diameter,
                    'plate_thickness': that_env.plate_thickness,
                    'oil_viscosity': that_env.oil_viscosity,
                    'initial_micro_polarity': that_env.initial_micro_polarity,
                    'surface_roughness': that_env.surface_roughness,
                    'rough_density': that_env.rough_density
                }
            })
        return tmp_arr
