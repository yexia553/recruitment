from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Q
from interview.models import Candidate
from interview import candidate_fieldstes as cf
import logging
from datetime import datetime
import csv
# Register your models here.

# 定义日志类，并获取当前代码文件的名字
logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school',
                     'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result',
                     'second_interviewer_user', 'hr_result',
                     'hr_score', 'hr_remark', 'hr_interviewer_user')


# define export action
def export_model_as_csv(modeladmin, request, queryset):
    """
    导出页面上选中的候选人信息
    :param modeladmin:
    :param request:
    :param queryset: 表示页面上选择的信息查询集
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头,获取fields_list中每个字段对应的verbose_name 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )

    for obj in queryset:
        # 单行的记录——各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info('%s exported %s candidates info.' % (request.user, len(queryset)))
    return response


# 定义export_model_as_csv在admin页面上显示的名称
export_model_as_csv.short_description = '导出为CSV文件'
export_model_as_csv.allowed_permissions = ('export',)


class CandidateAdmin(admin.ModelAdmin):
    # actions 可以为admin后台添加额外的功能，list中指向一个函数
    actions = [export_model_as_csv, ]
    exclude = ('creator', 'created_date', 'modified_date')

    list_display = ('username', 'city', 'bachelor_school',
                    'first_score', 'first_result',
                    'first_interviewer_user', 'second_score',
                    'second_result', 'second_interviewer_user',
                    'hr_score', 'hr_result', 'hr_interviewer_user',)
    # 设置搜索字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')
    # 设置筛选字段
    list_filter = ('city', 'first_result', 'second_result', 'hr_result',
                   'first_interviewer_user', 'second_interviewer_user',
                   'hr_interviewer_user')
    # 设置排序字段
    ordering = ('hr_result', 'second_result', 'first_result')

    def has_export_permission(self, request):
        """
        检查当前用户是否有导出权限
        1. self.opts获取当前访问的模型类的类名，比如这里是interview app中的candidate类，
        所以self.opts = interview.candidate
        2. opts.app_label 获取当前所在app的名称，这里就是interview
        3. 思考： 鉴于第二点，所以django中的权限是按照app级别区分的，而不是模型类区分的？
        :param request:
        :return:
        """
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    def get_fieldsets(self, request, obj=None):
        """
        设置权限，一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈;
        这个函数有个bug，当一面和二面的面试官是同一个人的时候，面试官只能看到default_fieldsets_first的信息，

        :param request:
        :param obj:表示页面上选中的候选人对象
        :return:
        """
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        if 'hr' in group_names or request.user.is_superuser:
            return cf.default_fieldsets
        return ()

    def get_queryset(self, request):
        """
        对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
        :param request:
        :return:
        """
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    def get_group_names(self, user):
        """
        获取用户的组名信息
        :param user: 在admin中可以使用user，感觉类似于views中request.User，
        具体有哪些参数可以使用pycharm debug模式中的Evaluate功能查看
        :return:
        """
        print(user)
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        """
        根据用户所属组是否为HR或者面试官，返回不同的readonly_field信息；
        一面和二面的面试官信息只有HR可以设置，面试官不可以，
        所以'first_interviewer_user'和'second_interviewer_user'对于面试官来说应该是只读的
        :param request:
        :param obj:
        :return:
        """
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user')
        return ()

    def get_list_editable(self, request):
        """
        根据用户的所属组来决定返回什么样的list_editable，
        只有当用户属于hr组的时候才可以编辑'first_interviewer_user', 'second_interviewer_user'
        list_editable字段可以让用户直接在导航页面就可以编辑相关字段，而不用点击到详情页面，适合批量操作
        :param request:
        :return:
        """
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    def get_changelist_instance(self, request):
        """
        override admin method and list_editable property value
        with values returned by our custom method implementation.
        django 的admin中原生不支持通过函数的方法返回list_editable字段，
        修改父类中get_changelist_instance方法使其支持该功能
        """
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)


admin.site.register(Candidate, CandidateAdmin)
# 设置页面标题
admin.site.site_header = "招聘系统"
