import os
import logging
import time

def logger_init(log_path, level):
    #创建一个logger
    logger = logging.getLogger()
    #log 等级总开关
    logger.setLevel(logging.INFO)

    #创建一个handler
    local_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    logfile = log_path + '/' + local_time + '.log'
    fh = logging.FileHandler(logfile, mode = 'w')
    fh.setLevel(logging.DEBUG)
    #定义输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

