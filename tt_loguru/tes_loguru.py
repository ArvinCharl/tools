#!/user/bin/env python3
# -*- coding: utf-8 -*-
from loguru import logger as log

# 指定日志格式
my_format = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {line} | {message} '

# 指定过滤器,将不同级别的日志保存到不同文件下
my_info_filter = lambda record: "INFO" in record['level'].name
my_error_filter = lambda record: "ERROR" in record['level'].name

# rotation:
# ① 限制日志大小: x KB/MB/GB
# ② 限制日志时间长度: Second/Minute/Hour/Day/Week/Month/Year 12:00:00
# ③ 例如: rotation="1 KB" 即保持该日志文件大小始终为1KB,若超过,则将之前1KB大小内容打包成新的一份。此时设置retention=1可仅保存额外的最新的一份。
# retention: 保留额外 n 份
log.add('INFO.log', rotation="1 Month", retention=1, format=my_format, filter=my_info_filter, backtrace=True,
        diagnose=True)
log.add('ERROR.log', rotation="1 Month", retention=1, format=my_format, filter=my_error_filter, backtrace=True,
        diagnose=True)


# 使用示例一
def tes_try_except(x, y):
    try:
        return x / y
    except:
        # 二选一即可
        log.exception('the_exception: 分母不能为"0"')  # 该方法通过 log.add(backtrace=True, diagnose=True) 记录详细错误内容
        log.error('the_error: 分母不能为"0"')  # 该方法仅记录'the_error: 分母不能为"0"'


# 使用示例二
@log.catch  # 记录该函数中错误详细内容
def tes_decorator(x, y):
    return x / y


if __name__ == '__main__':
    for i in range(1):
        log.debug('调试消息')
        log.info('普通消息')
        log.warning('警告消息')
        log.error('错误消息')
        log.critical('严重错误消息')
        log.success('成功调用')
        tes_try_except(1, 0)
        tes_decorator(1, None)
