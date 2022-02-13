# coding=utf-8
from Config import CommonConfig
import os
import time
import Utils
import Walk


# 机器人别摸了后要做什么？
def touched_do():
    if CommonConfig.IS_DEBUG_MODEL:
        # Utils.say('嘿嘿嘿...')  # 本地运行
        Utils.say('stand by')  # NAO机器人运行
    else:
        Utils.say('stand by')  # NAO机器人运行
    start_time = time.time()
    Walk.start()
    end_time = time.time()
    cost_time = end_time - start_time
    print '从听到哨声到跑完共花费时间：{}秒'.format(cost_time)


if __name__ == '__main__':
    if not os.path.exists('C:'):
        CommonConfig.IS_DEBUG_MODEL = False
    Utils.say('start...')
    while True:
        is_touched = Utils.get_is_touched()  # 获取头是否被摸了
        if is_touched == 1:  # 如果被摸了就可以停止监听并开始做
            break
    touched_do()
