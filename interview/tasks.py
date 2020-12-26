from celery import shared_task
from django.core.mail import send_mail
import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_interview_notify(candidates, send_to):
    subject = '面试通知'
    body = '%s 进入出面，请您准备进行面试' % candidates
    send_from = '1906390603@qq.com'

    try:
        # 如果邮件发送成功则返回 1
        res = send_mail(subject, body, send_from, send_to)
    except Exception as err:
        print(err)
