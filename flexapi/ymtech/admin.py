from django.contrib import admin
from ymtech.models.origin import *
from ymtech.models.csv import *
from ymtech.models.env import *

# Register your models here.


class CommonOriginAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'power', 'enabled', 'modified_at')
    search_fields = ['host', 'name', 'comments']
    list_filter = ['enabled']
admin.site.register(CommonOriginModel, CommonOriginAdmin)


class CommonEnvDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin', 'modified_at')
    search_fields = ['name', 'comments']
    list_filter = ['origin']
admin.site.register(CommonEnvDataModel, CommonEnvDataAdmin)


class CommonCsvDataAdmin(admin.ModelAdmin):
    list_display = ('env', 'index_time')
    search_fields = ['comments']
    list_filter = ['env']
admin.site.register(CommonCsvDataModel, CommonCsvDataAdmin)
