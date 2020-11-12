from django.contrib import admin
from jobs.models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date',)
    # exclude 可以设置 在编辑页面中不显示哪些字段，
    exclude = ('creator', 'created_date', 'modified_date',)

    # 由于creator字段没有在编辑页面中展示，也没有在model中设置默认值，所以需要为其赋值，设为当前登录的用户
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
