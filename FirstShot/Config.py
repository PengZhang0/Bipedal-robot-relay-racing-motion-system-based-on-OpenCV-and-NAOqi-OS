# coding=utf-8
import os

_BASE_PATH = os.path.abspath('.')  # 项目地址，如果是在NAO机器人上运行时这一项可以忽略


class CommonConfig(object):  # 公共配置类
    IS_DEBUG_MODEL = True  # 如果这一项是True,则说明是在自己电脑运行，否则说明是在NAO机器人上运行
    PORT = 9559  # 连接机器人的端口号
    IP = '192.168.43.205'

    CANT_CONNECT_SAY = 'cant connect to robot.'  # 如果在创建指令盒过程中失败，则认为是连接机器人失败，这个时候就会在控制台上打印这一个变量
    USERNAME = 'nao'  # 机器人系统账号
    PASSWORD = 'nao'  # 机器人密码
    TCP_PORT = 1493
    TCP_IP = '192.168.43.209'


class ListenConfig(object):  # 哨声检测相关的参数类
    RECORD_PATH = '/home/nao/record.wav'  # NAO机器人录音文件地址
    LOCAL_PATH = os.path.join(_BASE_PATH, 'record.wav')  # NAO机器人录音后上传到本机的文件地址
    RECORD_DELAY = 0.5  # 录音时间，每次录音录RECORD_DELAY秒，让后发送到主机识别响度
    RECORD_PASSAGEWAY = (0, 0, 1, 0)  # 录音通道
    RECORD_FREQUENCY = 16000  # 录音频率
    RECORD_TYPE = 'wav'  # 音频保存文件格式
    LOUDNESS_THRESHOLD = 30000  # 响度阈值，这个值越大，则唤醒机器人所需要的音量越大


class WalkConfig(object):  # 走路配置
    INIT_RUN_COUNT = 15  # 初始调整走的步长
    RUN_COUNT = 450  # 走的步长
    # 步伐参数配置
    g_moveConfig6 = [["MaxStepX", 0.04], ["MaxStepY", 0.13], ["MaxStepTheta", 0.4], ["MaxStepFrequency", 0.5],
                     ["StepHeight", 0.02], ["TorsoWx", 0.0], ["TorsoWy", 0.0]]  # 接力赛参数 长距离直走move1

    g_moveConfig7 = [
        ["MaxStepX", 0.08],  # 步长 0.001-0.08
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.95],  # 最大步频
        ["StepHeight", 0.013],  # 抬脚高度
        ["TorsoWx", 0.0],
        ["TorsoWy", 0.03]
    ]  # 接力赛参数 长距离直走move1
