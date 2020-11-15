from django.contrib import admin
from django.http import HttpResponse
from interview.models import Candidate
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
    # fieldsets 可以让admin管理页面把信息进行分组，展示的更加清晰
    fieldsets = (
        ('基础信息', {'fields': ('userid', 'username', 'city', 'phone',
                             'email', 'apply_position', 'born_address',
                             'gender', 'candidate_remark', 'bachelor_school',
                             'master_school', 'doctor_school', 'major',
                             'degree', 'test_score_of_general_ability',
                             'paper_score', 'last_editor',)}),
        ('第一轮面试记录', {'fields': ('first_score', 'first_learning_ability',
                                'first_professional_competency', 'first_advantage',
                                'first_disadvantage', 'first_result',
                                'first_recommend_position',
                                'first_interviewer_user', 'first_remark')}),
        ('第二轮面试记录', {'fields': ('second_score', 'second_learning_ability',
                                'second_professional_competency',
                                'second_pursue_of_excellence',
                                'second_communication_ability',
                                'second_pressure_score', 'second_advantage',
                                'second_disadvantage', 'second_result',
                                'second_recommend_position', 'second_interviewer_user',
                                'second_remark',)}),
        ('HR面试记录', {'fields': ('hr_score', 'hr_responsibility', 'hr_communication_ability',
                               'hr_logic_ability', 'hr_potential', 'hr_stability',
                               'hr_advantage', 'hr_disadvantage', 'hr_result',
                               'hr_interviewer_user', 'hr_remark')})
    )


admin.site.register(Candidate, CandidateAdmin)
