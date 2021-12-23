from multiprocessing.dummy import JoinableQueue
from django.contrib import admin
from .models import Jobhdr, Femast, Feasoc, Jobtas, Orgtbl


@admin.register(Jobhdr)
class JobhdrAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'job_status')
    list_filter = ('job_status', 'work_type', 'target_end_date')

@admin.register(Jobtas)
class JobtasAdmin(admin.ModelAdmin):
    list_display = ('job_num', 'task_status')
    list_filter = ('task_status', 'task_num')

@admin.register(Orgtbl)
class OrgtblAdmin(admin.ModelAdmin):
    list_display = ('id', 'orgn_code')


@admin.register(Femast)
class FemastAdmin(admin.ModelAdmin):
    list_display = ('fe_key', 'fe_type')
    list_filter = ('fe_type', 'vet_flag')
    search_fields = ('fe_key', 'id')


@admin.register(Feasoc)
class FeasocAdmin(admin.ModelAdmin):
    list_display = ('parent_fe_id', 'child_fe_id', 'vet_flag')
    list_filter = ('parent_fe_id', 'child_fe_id', 'vet_flag')






