"""
说明：
url(r'job/(?P<job_id>\d+)$', views.job_detail, name='job_detail'),
这一行代码原本在url最后没有添加$符号，也就是没有限定url的结尾，
导致在admin的界面想要点击job_name或者job_id进行修改的时候，
由于url是/job/id/change，先被上面的模式匹配到，跳转到job_detail页面，而不是修改页面，
在url最后添加了$表示url完全匹配/job/id/这种模式的时候才回跳转到job_detail，
所以最好实在url后面都加上$。
"""
from django.conf.urls import url
from django.urls import path

from jobs import views

urlpatterns = [
    url(r'^joblist/', views.job_list, name='job_list'),
    # url中使用括号来捕捉参数，通过?P<>来命名
    url(r'job/(?P<job_id>\d+)/$', views.job_detail, name='job_detail'),
    path(r'resume/add/', views.ResumeCreateView.as_view(), name='resume_add'),
    path(r'resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),
    # 设置首页，跳转到职位列表
    url(r'^$', views.job_list, name='index'),
]