# coding:utf-8

import time
import json
from ymtech.models.origin import *
from ymtech.models.env import *
from ymtech.models.csv import *
from django.shortcuts import render
from django.http import HttpResponse

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
