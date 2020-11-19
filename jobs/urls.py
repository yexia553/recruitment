from django.conf.urls import url
from django.urls import path

from jobs import views

urlpatterns = [
    url(r'^joblist/', views.job_list, name='job_list'),
    # url中使用括号来捕捉参数，通过?P<>来命令
    url(r'job/(?P<job_id>\d+)', views.job_detail, name='job_detail'),
    path(r'resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    # 设置首页，跳转到职位列表
    url(r'^$', views.job_list, name='index'),
]
