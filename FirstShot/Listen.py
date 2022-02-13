# coding=utf-8
import Walk
import time
import NewWalk
import Utils
import numpy as np
from threading import Lock, Thread, Event
from Config import CommonConfig, ListenConfig, WalkConfig
import wave


# if CommonConfig.IS_DEBUG_MODEL:
#     from matplotlib import pyplot as plt

# flag = 1  # 信号指示灯，如果某一时刻的响度大于这个阈值，flag会变成0，代表机器人可以开跑了
# lock = Lock()  # 锁对象，用于同步
# event = Event()


def function():
    while True:
        print 'start recording...'
        try:
            Utils.record.startMicrophonesRecording(
                ListenConfig.RECORD_PATH,  # 录音文件保存地址
                ListenConfig.RECORD_TYPE,  # 录音保存格式
                ListenConfig.RECORD_FREQUENCY,  # 录音频率
                ListenConfig.RECORD_PASSAGEWAY  # 录音通道
            )
        except BaseException as e:
            print e
            Utils.record.stopMicrophonesRecording()
            Utils.record.startMicrophonesRecording(
                ListenConfig.RECORD_PATH,  # 录音文件保存地址
                ListenConfig.RECORD_TYPE,  # 录音保存格式
                ListenConfig.RECORD_FREQUENCY,  # 录音频率
                ListenConfig.RECORD_PASSAGEWAY  # 录音通道
            )
        time.sleep(ListenConfig.RECORD_DELAY)  # 延迟，录音
        Utils.record.stopMicrophonesRecording()  # 结束录音
        if CommonConfig.IS_DEBUG_MODEL:
            Utils.get_file(ListenConfig.RECORD_PATH, ListenConfig.LOCAL_PATH)  # NAO机器人上传文件到本地
        else:
            pass  # 如果在NAO机器人上运行的话就什么也不做
        print 'record over'
        #######################################################################
        print 'get loudness begin...'
        try:
            if CommonConfig.IS_DEBUG_MODEL:
                f = wave.open(ListenConfig.LOCAL_PATH, "rb")  # Debug模式，在本地找文件
            else:
                f = wave.open(ListenConfig.RECORD_PATH, "rb")  # 非Debug模式，在NAO机器人上找文件
            frames = f.getnframes()  # 读取帧数
            str_data = f.readframes(frames)  # 读取全部帧
            f.close()
            wave_data = np.fromstring(str_data, dtype=np.int16)  # 获取正弦波列表
            max_score = wave_data.max()  # 最大响度
            print '最大响度为', max_score
            # if CommonConfig.IS_DEBUG_MODEL:  # 如果是Debug模式，则会显示声波图
            #     x = range(1, wave_data.__len__() + 1)
            #     plt.plot(x, wave_data)
            #     plt.show()
            if max_score > ListenConfig.LOUDNESS_THRESHOLD:  # 判断当前最大响度是否大于阈值
                break
        except BaseException as e:
            print e
        print 'get loudness over'


def run():  # 运行函数
    Walk.rest()
    Utils.say('in monitor...')
    function()  # 监听哨声
    # Utils.say('Go...')  # 听到哨声要做的事
    # start_time = time.time()
    # Walk.move(WalkConfig.INIT_RUN_COUNT, 0, 0, WalkConfig.g_moveConfig6)  # 初始化调整
    # time.sleep(1)
    Walk.run()  # 开跑！
    Utils.send_massage()
    # end_time = time.time()
    # cost_time = end_time - start_time
    # print '从听到哨声到跑完共花费时间：{}秒'.format(cost_time)