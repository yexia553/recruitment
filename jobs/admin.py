from django.contrib import admin
from jobs.models import Job, Resume


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date',)
    # exclude 可以设置 在编辑页面中不显示哪些字段，
    exclude = ('creator', 'created_date', 'modified_date',)

    # 由于creator字段没有在编辑页面中展示，也没有在model中设置默认值，所以需要为其赋值，设为当前登录的用户
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major','created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience", "project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        """
        把applicant保存成当前登录的用户
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)
