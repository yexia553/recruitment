"""
定义一个简单的celery异步任务
"""
from celery import Celery


# 第一个参数 是当前脚本的名称，第二个参数 是 broker 服务地址
app = Celery('tasks', backend='redis://127.0.0.1', broker='redis://127.0.0.1')


@app.task()
def add(x, y):
    return x + y
