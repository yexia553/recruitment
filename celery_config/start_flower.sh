# 启动celery的监控工具flower，默认端口是5555
# 详细可参考文档：https://docs.celeryproject.org/en/stable/userguide/monitoring.html
celery --app=tasks flower --broker=redis://127.0.0.1:6379/0