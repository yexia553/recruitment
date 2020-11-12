from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404

from jobs.models import Job
from jobs.models import Cities
from jobs.models import JobTypes


def job_list(request):
    """
    职位列表
    :param request:
    :return:
    """
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {
        'job_list': job_list
    }

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    return HttpResponse(template.render(context))


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

