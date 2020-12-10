celery 在3.1版本之后就原生支持Django，不再需要其他包。  
参考官网链接：[Celery Django 配置](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)  

### 注意
官网教程只需要在proj/proj/__init__.py里面添加以下代码以便
在django启动的时候会自动导入celery app，但是实际上也需要在
django每个app的__init__.py中都需添加以下代码
```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```