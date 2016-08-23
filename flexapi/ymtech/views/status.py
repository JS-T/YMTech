# coding:utf-8

import time
import json
from ymtech.models.origin import *
from ymtech.models.env import *
from ymtech.models.csv import *
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.


def alive(request):
    return HttpResponse(json.dumps({
        'status': 200,
        'message': 'Hello world!',
        'timestamp': int(time.time())
    }, indent=4), content_type='application/json')


def origin(request):
    origin_list = CommonOriginModel.status_origin()
    return HttpResponse(json.dumps({
        'status': 200,
        'origin': origin_list,
        'timestamp': int(time.time())
    }, indent=4), content_type='application/json')


def env(request, origin_id):
    that_origin = CommonOriginModel.objects.filter(id=int(origin_id))
    if that_origin:
        that_origin = that_origin[0]
        env_list = CommonEnvDataModel.status_env(that_origin)
    else:
        env_list = []
    return HttpResponse(json.dumps({
        'status': 200,
        'origin': origin_id,
        'env': env_list,
        'timestamp': int(time.time())
    }, indent=4), content_type='application/json')


def csv(request, env_id):
    that_env = CommonEnvDataModel.objects.filter(id=int(env_id))
    if that_env:
        that_env = that_env[0]
        csv_content = CommonCsvDataModel.download_csv(that_env)
    else:
        csv_content = ''
    response = StreamingHttpResponse(streaming_content=csv_content)
    name = that_env.name
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(name.encode('utf-8'))
    return response
