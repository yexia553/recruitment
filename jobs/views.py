from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from jobs.models import Job
from jobs.models import Cities
from jobs.models import JobTypes
from jobs.models import Resume


def job_list(request):
    """
    职位列表
    :param request:
    :return:
    """
    job_list = Job.objects.order_by('job_type')
    context = {
        'job_list': job_list
    }

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    return render(request, 'joblist.html', context)


def job_detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        content = {
            'job': job
        }
    except Job.DoesNotExist:
        raise Http404('Job Does Not Exist!')
    return render(request, 'job.html', content)


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView 是Django自带的可以创建model实例对象的视图方法，常见的还有ListView等
    """
    # 指明作用于哪一个model
    model = Resume
    template_name = 'resume_form.html'
    # 创建成功后重定向到该url
    success_url = '/joblist/'
    # 需要填写的字段
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]


class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'resume_detail.html'
