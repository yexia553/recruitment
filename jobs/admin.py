from django.contrib import admin
from django.contrib import messages
from jobs.models import Job, Resume
from interview.models import Candidate
from datetime import datetime


# 通过装饰器来配置admin页面
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date',)
    # exclude 可以设置 在编辑页面中不显示哪些字段，
    exclude = ('creator', 'created_date', 'modified_date',)
    # 定义哪些字段可以点击进去进行内容修改
    list_display_links = ('id', 'job_name')

    def save_model(self, request, obj, form, change):
        """
        由于creator字段没有在编辑页面中展示，
        也没有在model中设置默认值，所以需要为其赋值，
        设为当前登录的用户
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.creator = request.user
        super().save_model(request, obj, form, change)


def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ''
    for resume in queryset:
        candidate = Candidate()
        # 把resume的属性都赋值给candidate
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names += candidate.username + ', '
        candidate.save()
    # 这个函数激活的时候在页面上展示一条消息
    messages.add_message(request, messages.INFO, '候选人%s已经进入面试流程' % candidate_names)


enter_interview_process.short_description = '进入面试流程'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    actions = (enter_interview_process, )

    list_display = ('username', 'applicant', 'city', 'apply_position',
                    'bachelor_school', 'master_school', 'major', 'created_date')

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


# 也可以通过这种方式来应用admin配置，但是装饰器更灵活，与admin类在一起，阅读更容易
# admin.site.register(Job, JobAdmin)
# admin.site.register(Resume, ResumeAdmin)
