from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_enter_interview_info(candidates,):
    subject = '面试通知'
    body = '%s 进入出面，请准备面试' % candidates
    send_from = '1906390603@qq.com'
    send_to = ['1906390603@qq.com']

    send_mail(subject, body, send_from, send_to)



