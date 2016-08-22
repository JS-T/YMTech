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

    @staticmethod
    def download_csv(that_env):
        all_csv = CommonCsvDataModel.objects.filter(env=that_env).order_by('id')
        content = "实验编号\n"
        content += that_env.name + "\n"
        content += "初始转速,设定压力,转动惯量,摩擦片面数\n"
        content += str(that_env.initial_speed) + ','
        content += str(that_env.setting_pressure) + ','
        content += str(that_env.rotary_inertia) + ','
        content += str(that_env.sides_count) + "\n"
        content += "温度,摩擦片内径,摩擦片外径,摩擦片厚度,润滑油粘度,初始油膜厚度,摩擦材表面粗糙度,粗糙密度\n"
        content += str(that_env.temperature) + ','
        content += str(that_env.inner_diameter) + ','
        content += str(that_env.outer_diameter) + ','
        content += str(that_env.plate_thickness) + ','
        content += str(that_env.oil_viscosity) + ','
        content += str(that_env.initial_micro_polarity) + ','
        content += str(that_env.surface_roughness) + ','
        content += str(that_env.rough_density) + "\n"
        content += "indextime,Tc,Finmin/10,w_rel/100,h*100000,muu\n"
        for csv in all_csv:
            content += str("%.6f" % csv.index_time) + ','
            content += str("%.6f" % csv.torque) + ','
            content += str("%.6f" % (csv.pressure / 10)) + ','
            content += str("%.6f" % (csv.speed / 100)) + ','
            content += str("%.6f" % (csv.micro_polarity * 100000)) + ','
            content += str("%.6f" % csv.dynamic_friction_coefficient) + "\n"
        return content + "\n"
