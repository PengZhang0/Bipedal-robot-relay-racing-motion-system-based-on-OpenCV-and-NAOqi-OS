# coding=utf-8
import socket
from naoqi import ALProxy
from Config import CommonConfig
from Config import WalkConfig
import time

memory = ALProxy("ALMemory", CommonConfig.IP, CommonConfig.PORT)  # 内存代理
tts = ALProxy("ALTextToSpeech", CommonConfig.IP, CommonConfig.PORT)  # 说话代理
record = ALProxy('ALAudioRecorder', CommonConfig.IP, CommonConfig.PORT)  # 录音指令盒
motion = ALProxy("ALMotion", CommonConfig.IP, CommonConfig.PORT)  # 移动模块
posture = ALProxy("ALRobotPosture", CommonConfig.IP, CommonConfig.PORT)  # 姿势模块
camera = ALProxy("ALVideoDevice", CommonConfig.IP, CommonConfig.PORT)  # 摄像头管理模块


# 获取机器人是否被触摸了
def get_is_touched():
    if memory.getData("FrontTactilTouched") == 1:  # 获取机器人头部（最前面那一片）的
        return 1
    elif memory.getData("MiddleTactilTouched") == 1:  # 获取机器人头部（中间那一片）的
        return 1
    elif memory.getData("RearTactilTouched") == 1:  # 获取机器人头部（最后面那一片）的
        return 1
    else:
        return 0


# 说话
def say(content):
    tts.say(content)


# 发送套接字
def send_massage():
    if CommonConfig.IS_DEBUG_MODEL:
        IP = '127.0.0.1'  # 填写服务器端的IP地址
    else:
        IP = CommonConfig.TCP_IP
    port = CommonConfig.TCP_PORT  # 端口号必须一致
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP, port))
    except Exception as e:
        print e
        print('server not find or not open')
        return
    trigger = 'Go'
    s.sendall(trigger.encode())
    s.close()


def moveTo(x=0, y=0, theta=0.0, config=WalkConfig.g_moveConfig7):
    motion.moveToward()


if __name__ == '__main__':
    say('嘿嘿嘿')
    send_massage()
