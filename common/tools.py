# -*- coding: utf-8 -*-
from ext import redisHelper
import time

redis = redisHelper()


def code_send_limit(key,n=3):
    '''
    :param key: key可为手机号或邮箱，存入redis list中
    :param n: 限制次数
    :return: True:已达到限制，False:不限制
    '''
    # 去除空格并小写
    key = key.strip().lower()
    length = redis.llen(key)
    # 超过指定次数，限制
    if length < n:
        redis.lpush(key, int(time.time()))
        return False
    else:
        # 校验时间间隔
        last_time = int(redis.lindex(key, 0))
        if int(time.time()) - last_time < 10*60:
            return True
        else:
            return False