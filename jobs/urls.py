from django.conf.urls import url

from jobs import views

urlpatterns = [
    url(r'^joblist/', views.job_list, name='jobl_ist'),
    # url中使用括号来捕捉参数，通过?P<>来命令
    url(r'job/(?P<job_id>\d+)', views.job_detail, name='job_detail'),
]
