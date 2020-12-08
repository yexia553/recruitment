"""
使用函数的方法自定义一个django中间件,该中间件记录服务器处理一个请求的耗时
"""
import time
import logging


logger = logging.getLogger(__name__)


def performance_logger_middleware(get_response):
    def middleware(request):
        """
        计算django处理一个请求的时间，作为请求头返回给浏览器，并记录到日志中
        :param request:
        :return:
        """
        start_time = time.time()
        response = get_response(request)
        duration = (time.time() - start_time)*1000
        response['X-Page-Duration-ms'] = duration
        logger.info('%s  %s  %s' % (duration, request.path, request.GET.dict()))
        return response

    return middleware
