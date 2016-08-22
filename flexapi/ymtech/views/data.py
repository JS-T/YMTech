# coding:utf-8

import time
import json
from ymtech.models.origin import *
from ymtech.models.csv import *
from ymtech.models.env import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden

# Create your views here.


def submit(request):
    that_post = request.body
    if len(that_post) == 0:
        return HttpResponseForbidden(json.dumps({
            'status': 400,
            'message': 'Empty POST.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    that_content = that_post.decode('gbk').encode('utf-8')
    that_get = request.GET
    if 'secret' not in that_get:
        return HttpResponseForbidden(json.dumps({
            'status': 403,
            'message': 'Empty secret.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    that_secret = that_get['secret']
    that_origin = CommonOriginModel.objects.filter(secret=that_secret)
    if not that_origin:
        return HttpResponseForbidden(json.dumps({
            'status': 403,
            'message': 'Invalid origin.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    else:
        that_origin = that_origin[0]
    that_content = that_content.split('\n')
    if len(that_content) < 7:
        return HttpResponseServerError(json.dumps({
            'status': 502,
            'message': 'Malformed LENGTH.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    that_env_name = that_content[1]
    line_3 = that_content[3]
    line_3_arr = line_3.split(',')
    if len(line_3_arr) != 4:
        return HttpResponseServerError(json.dumps({
            'status': 502,
            'message': 'Malformed LINE 4.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    line_5 = that_content[5]
    line_5_arr = line_5.split(',')
    if len(line_5_arr) != 8:
        return HttpResponseServerError(json.dumps({
            'status': 502,
            'message': 'Malformed LINE 6.',
            'timestamp': int(time.time())
        }, indent=4), content_type='application/json')
    CommonEnvDataModel.objects.update_or_create(
        name=that_env_name,
        origin=that_origin,
        initial_speed=float(line_3_arr[0]),
        setting_pressure=float(line_3_arr[1]),
        rotary_inertia=float(line_3_arr[2]),
        sides_count=float(line_3_arr[3]),
        temperature=float(line_5_arr[0]),
        inner_diameter=float(line_5_arr[1]),
        outer_diameter=float(line_5_arr[2]),
        plate_thickness=float(line_5_arr[3]),
        oil_viscosity=float(line_5_arr[4]),
        initial_micro_polarity=float(line_5_arr[5]),
        surface_roughness=float(line_5_arr[6]),
        rough_density=float(line_5_arr[7])
    )
    that_env = CommonEnvDataModel.objects.filter(name=that_env_name)
    that_env = that_env[0]
    count = 0
    for i in range(7, len(that_content) - 1):
        line = that_content[i]
        line_arr = line.split(',')
        col_count = len(line_arr)
        if col_count < 1 or col_count > 6:
            return HttpResponseServerError(json.dumps({
                'status': 502,
                'message': 'Malformed LINE ' + str(i + 1) + '.',
                'timestamp': int(time.time())
            }, indent=4), content_type='application/json')
        new_csv = CommonCsvDataModel()
        new_csv.env = that_env
        new_csv.index_time = float(line_arr[0])
        if col_count > 1:
            new_csv.torque = float(line_arr[1])
        if col_count > 2:
            new_csv.pressure = float(line_arr[2]) * 10
        if col_count > 3:
            new_csv.speed = float(line_arr[3]) * 100
        if col_count > 4:
            new_csv.micro_polarity = float(line_arr[4]) / 100000
        if col_count > 5:
            new_csv.dynamic_friction_coefficient = float(line_arr[5])
        new_csv.save()
        count += 1
    return HttpResponse(json.dumps({
        'status': 200,
        'env': that_env.id,
        'count': count,
        'timestamp': int(time.time())
    }, indent=4), content_type='application/json')
