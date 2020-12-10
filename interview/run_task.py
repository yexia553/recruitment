"""
执行一个简单的celery任务；
简易使用pycharm的调试功能查看result有哪些方法可供使用，
"""
from interview.tasks import add

result = add.delay(4, 4)
print('Is task ready: %s' % result.ready())

run_result = result.get(timeout=1)
print('task result: %s' % run_result)
