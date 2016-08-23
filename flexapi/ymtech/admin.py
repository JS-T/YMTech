# coding:utf-8

import sys
import time
import zipfile
from django.contrib import admin
from ymtech.models.csv import *
from ymtech.models.env import *
from django.http import StreamingHttpResponse

reload(sys)
sys.setdefaultencoding('utf-8')

# Register your models here.


def export_as_csv(model_admin, request, queryset):
    def file_iterator(filename, chunk_size=512):
        with open(filename) as fp:
            while True:
                c = fp.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    if len(queryset) == 1:
        that_env = queryset[0]
        response = StreamingHttpResponse(
            streaming_content=CommonCsvDataModel.download_csv(that_env)
        )
        name = that_env.name + '.csv'
    else:
        zip_name = '/tmp/bundles_' + str(int(time.time())) + '.zip'
        f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        for that_env in queryset:
            content = CommonCsvDataModel.download_csv(that_env)
            name = that_env.name + '.csv'
            file_name = '/tmp/' + name.encode('utf-8')
            file_object = open(file_name, 'w')
            file_object.write(content)
            file_object.close()
            f.write(file_name)
        f.close()
        response = StreamingHttpResponse(file_iterator(zip_name))
        name = "bundles.zip"
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(name.encode('utf-8'))
    return response
export_as_csv.short_description = u"另存为 csv 格式"


class CommonOriginAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'power', 'enabled', 'modified_at')
    search_fields = ['host', 'name', 'comments']
    list_filter = ['enabled']
admin.site.register(CommonOriginModel, CommonOriginAdmin)


class CommonEnvDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin', 'modified_at')
    search_fields = ['name', 'comments']
    list_filter = ['origin']
    actions = [export_as_csv]
admin.site.register(CommonEnvDataModel, CommonEnvDataAdmin)


class CommonCsvDataAdmin(admin.ModelAdmin):
    list_display = ('env', 'index_time')
    search_fields = ['comments']
    list_filter = ['env']
admin.site.register(CommonCsvDataModel, CommonCsvDataAdmin)
