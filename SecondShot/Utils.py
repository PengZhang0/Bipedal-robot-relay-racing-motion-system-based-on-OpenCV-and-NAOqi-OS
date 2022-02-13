# coding=utf-8
import socket
import time
from naoqi import ALProxy
from Config import CommonConfig

memory = ALProxy("ALMemory", CommonConfig.IP, CommonConfig.PORT)  # 内存代理
tts = ALProxy("ALTextToSpeech", CommonConfig.IP, CommonConfig.PORT)  # 说话代理
record = ALProxy('ALAudioRecorder', CommonConfig.IP, CommonConfig.PORT)  # 录音指令盒


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


# tcp监听
def listen_tcp():
    say('正在监听一号机器人...')
    if CommonConfig.IS_DEBUG_MODEL:
        IP = 'localhost'
    else:
        IP = CommonConfig.IP  # 服务器端可以写"localhost"，可以为空字符串""，可以为本机IP地址
    # IP = 'localhost'
    port = CommonConfig.UDP_PORT  # 端口号
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, port))
    s.listen(1)
    print('listen at port :', port)
    conn, addr = s.accept()
    print('connected by', addr)

    data = conn.recv(1024)
    data = data.decode()  # 解码
    if not data:
        pass
    else:
        print('received message:', data)
    conn.close()
    s.close()


if __name__ == '__main__':
    say('嘿嘿嘿')
    listen_tcp()
