# coding=utf-8
import os
from Config import CommonConfig
import Listen
import Utils


# 机器人别摸了后要做什么？
def touched_do():
    if CommonConfig.IS_DEBUG_MODEL:
        Utils.say('冲...')  # 本地运行
    else:
        Utils.say('stand by')  # NAO机器人运行
    Listen.run()  # 开始监听哨声


if __name__ == '__main__':
    if not os.path.exists('C:'):
        CommonConfig.IS_DEBUG_MODEL = False
    Utils.say('start...')
    while True:
        is_touched = Utils.get_is_touched()  # 获取头是否被摸了
        if is_touched == 1:  # 如果被摸了就可以停止监听并开始做
            break
    touched_do()
