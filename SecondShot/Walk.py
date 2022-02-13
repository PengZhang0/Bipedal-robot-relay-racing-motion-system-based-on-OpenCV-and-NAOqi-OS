# -*- coding:utf-8 -*-
# 沿着白线边走边识别
# -*- coding:utf-8 -*-
import almath
import vision_definitions
import Utils
from naoqi import ALProxy
from PIL import Image
import time
import math
import cv2
import numpy as np
import logging

from Config import CommonConfig, WalkConfig

# IP及端口
IP = CommonConfig.IP
Port = 9559  # 每个端口都承载了不同的通信的作用

# 步伐参数配置
g_moveConfig = [["MaxStepX", 0.04], ["MaxStepY", 0.13], ["MaxStepTheta", 0.4], ["MaxStepFrequency", 0.5],
                ["StepHeight", 0.02], ["TorsoWx", 0.0], ["TorsoWy", 0.0]]  # 接力赛参数 长距离直走move1


# -----------------------------初始化相关-------------------------
# 初始化
def nao_init(Name, Ip):
    log_name = Name
    ip = Ip
    '''开始前机器人的初始化'''
    try:  # 为什么要弄一个判断机制？
        load_module(ip)
    except Exception, e1:
        print e1
        try:
            load_module()
        except Exception, e2:
            print e2
            exit(2)
    # 1、站起来
    global g_motion, g_posture
    g_posture.goToPosture("StandInit", 0.5)


# 加载所需模块 # 从存储模块的代理人中取走相应模块
def load_module(ip=IP, port=9559):  # global语句：在一个函数内修改全局变量
    global g_tts, g_motion, g_posture, g_memory, g_camera, g_SonarProxy, g_lock
    g_tts = ALProxy("ALTextToSpeech", ip, port)  # 说话模块      #应该是调用了函数     # 使用代理
    g_motion = ALProxy("ALMotion", ip, port)  # 移动模块    # 模块的名称
    g_posture = ALProxy("ALRobotPosture", ip, port)  # 姿势模块
    g_memory = ALProxy("ALMemory", ip, port)  # 内存管理模块
    g_camera = ALProxy("ALVideoDevice", ip, port)  # 摄像头管理模块
    g_SonarProxy = ALProxy("ALSonar", ip, port)  # 检测障碍物模块


def sonar():
    nao_init("NAOTwo", IP)

    g_SonarProxy.subscribe("location")  # 注册位置信息
    check_distance = 0.8  # 距离阈值，代表障碍物与机器人的距离
    while 1:
        left_value = g_memory.getData("Device/SubDeviceList/US/Left/Sensor/Value")  # 左接收器检测的距离
        right_value = g_memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")  # 右接收器检测的距离
        print(left_value, right_value)
        if (left_value <= check_distance) and (right_value <= check_distance):  # 根据左右两边的距离和阈值的关系进行判断
            # g_tts.say("unobstructed")
            g_tts.say("monitor robot pass")
            g_lock = 0
            break
        else:
            # g_tts.say("憨批")
            g_lock = 1
            g_tts.say("in test pass")
            # break
    g_SonarProxy.unsubscribe("location")


def move_line(distance=0.0):  # distance:距离长度

    global g_motion
    i = 0
    # 行走初始化
    print "开始行走初始化"
    # g_posture.goToPosture("StandInit", 0.5)
    # g_motion.moveInit()
    # 设置初始角度
    g_motion.setAngles('HeadPitch', 10 * math.pi / 180.0, 0.8)
    g_camera.setActiveCamera(1)  # 0是上摄像头 此处使用下摄像头, 如果激活成功返回值为true
    # g_camera.unsubscribe("AL::kBottomCamera")
    # Register a Generic Video Module注册通用视频模块
    resolution = vision_definitions.kQVGA
    color_space = vision_definitions.kBGRColorSpace
    fps = 30
    # g_camera.unsubscribe("AL::kBottomCamera")
    name_id = g_camera.subscribe("AL::kBottomCamera", resolution, color_space, fps)
    print "name_id is " + name_id
    # 名称 –订阅模块的名称。
    # 分辨率 -请求的分辨率。（请参阅支持的决议）
    # color_space –请求的色彩空间。（请参阅支持的色彩空间）
    # fps –向视频源请求的Fps（每秒帧数）。OV7670 VGA摄像机只能以30fps的速度运行，而MT9M114 HD摄像机在不久的将来将可以在某些特殊模式下更快地运行。
    # 设置曝光度模式
    g_camera.setCamerasParameter(name_id, 22, 2)
    print 'getting images in remote'  # 远程获取图像

    x = []
    y = []
    robot_position = g_motion.getRobotPosition(0)
    current_position = [0, 0, 0]
    n = 0
    while 1:
        n = n + 1
        # 获取机器人位置坐标，计算里程
        robot_new_position = g_motion.getRobotPosition(0)  # 返回一个包含世界绝对机器人位置的向量。
        # （以米为单位的绝对位置X，以米为单位的绝对位置Y，以弧度为单位的绝对角度Theta（Wz））。 Wz是] -pi，pi]之间的角度。
        current_position[0] = ((robot_new_position[0] - robot_position[0]) * 100) * math.cos(n) + (
                (robot_new_position[1] - robot_position[1]) * 100) * math.sin(n)  # 得到相对位移x
        current_position[1] = ((robot_new_position[1] - robot_position[1]) * 100) * math.cos(n) - (
                (robot_new_position[0] - robot_position[0]) * 100) * math.sin(n)  # 得到相对位移Y
        current_position[2] = (robot_new_position[2] - robot_position[2]) * 57.32  # 转换为弧度制
        x.append(current_position[0])
        y.append(current_position[1])
        print"current_position is :"
        print current_position
        ##########################
        i = i + 1
        print "getting image " + str(i)
        print name_id
        nao_image = g_camera.getImageRemote(name_id)
        image_width = nao_image[0]
        image_height = nao_image[1]
        array = nao_image[6]
        im = Image.frombytes("RGB", (image_width, image_height), array)  # 解析图片
        # -----------
        frame = np.asarray(im)  # ndarray是一个通用的同构数据多维容器，也就是说，其中的所有元素必须是相同类型的。
        # 对读取的图像矩阵进行计算，计算白线位置
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowera = np.array([0, 0, 221])
        uppera = np.array([180, 60, 255])
        mask1 = cv2.inRange(hsv, lowera, uppera)
        kernel = np.ones((4, 5), np.uint8)
        mask = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        newlines = cv2.HoughLines(mask, 1, np.pi / 180, 80)
        print "白线", newlines
        if newlines is None:
            print "NO LINE"
            newlines1 = [[0, 0]]
        else:
            # 找到白线
            newlines1 = newlines[:, 0, :]
            # newlines1 = newlines[0]
            print "newlines1", newlines1[0]
            # print "point line:",newlines1[0]
            for rho, theta in newlines1[:]:
                print "theta", theta
                a = np.cos(theta)
                b = np.sin(theta)
                print "a,b:-------------"
                print a, b
                x0 = a * rho
                y0 = b * rho
                print "x0,y0:"  # 起点坐标
                print x0, y0
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                print x1, y1
                print x2, y2
                # 画线
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 第一个参数 img：要划的线所在的图像;
            # 第二个参数 pt1：直线起点
        # 第三个参数 pt2：直线终点
        # 第四个参数 color：直线的颜色
        # 第五个参数 thickness=1：线条粗细
        single_line_value = newlines1[0]

        # newlines1[0]不等于0，说明检测到白线
        if single_line_value[0] != 0:
            # motionProxy.move(0.1,0,0,moveConfig)
            if single_line_value[1] <= 1.04:
                print "turn right"
                # 右转前进
                # g_motion.move(0.3, 0, -0.2, moveConfig)
                # g_motion.move(0.3, 0, -0.2, g_moveConfig6)
                g_motion.move(1, 0, -0.2, WalkConfig.g_moveConfig7)
            elif single_line_value[1] >= 2.09:
                print "turn left"
                # 左转前进
                # g_motion.move(0.3, 0, 0.2, moveConfig)
                # g_motion.move(0.3, 0, 0.2, g_moveConfig6)
                g_motion.move(1, 0, 0.2, WalkConfig.g_moveConfig7)
            else:
                print "mindle"
                # 识别到终点直线
                if 1.57 >= single_line_value[1] > 1.04:
                    # g_motion.move(0.3, 0, 0.1, g_moveConfig6)  # x –沿X轴的速度，以米/秒为单位。对后退运动使用负值
                    g_motion.move(1, 0, 0.1, WalkConfig.g_moveConfig7)  # x –沿X轴的速度，以米/秒为单位。对后退运动使用负值
                # y –沿Y轴的速度，以米/秒为单位。使用正值向左移动
                # theta –绕Z轴的速度，以弧度每秒为单位。使用负值顺时针旋转。
                # moveConfig –具有自定义移动配置的ALValue。
                if 2.09 >= single_line_value[1] > 1.57:
                    # g_motion.move(0.3, 0, -0.1, g_moveConfig6)
                    g_motion.move(1, 0, -0.1, WalkConfig.g_moveConfig7)
                # motionProxy.move(0.3,0.0,0.0,moveConfig)

        else:
            print "no line"
            if current_position[0] <= distance:
                # g_motion.move(0.1, 0.0, 0.0, g_moveConfig6)
                g_motion.move(0.8, 0.0, 0.0, WalkConfig.g_moveConfig7)
            else:
                # g_motion.move(0.0, 0.0, 0.0, g_moveConfig6)
                g_motion.move(0.0, 0.0, 0.0, WalkConfig.g_moveConfig7)
                print "我退出啦!"
                g_motion.rest()
                break
    g_camera.unsubscribe("AL::kBottomCamera")


# 移动函数，包装了api的移动，同时添加了一些修正
def move(x=0.0,
         y=0.0, theta=0.0, config=WalkConfig.g_moveConfig6):
    '''
    NAO移动：以FRAME_ROBOT坐标系为参照，theta为角度
    :param x: 前进后退 单位cm
    :param y: 左右移动 cm
    :param theta: 旋转角度，往左为正，单位度数
    :param config: 行走参数配置
    :return:
    '''
    global g_motion
    g_motion.moveInit()
    try:
        # 如果传入为小数，强转
        x1 = int(x + 0.5)
        x2 = round(x)
        y1 = round(y)
        theta1 = round(theta * almath.TO_RAD, 2)
        # 行走前初始化
        g_motion.moveInit()
        # 如果是往前走，修正
        step1 = x1 / 56
        # step2 = x1 % 56 / 20
        step3 = x1 % 56
        adjustY = 2
        # adjustTheta = 13
        adjustTheta = 3  # 16超级发热
        print ("step1 ", step1)
        # print("step2  ", step2)
        print("step3  ", step3)
        # 走至指定位置，解决走路偏斜问题
        # 第一段，走50cm
        if x1 > 0:
            for i in range(step1):
                g_motion.moveTo(56 * 0.01, 0, 0, config)
                g_motion.moveTo(0, 0, -adjustTheta * almath.TO_RAD, config)
                # g_motion.moveTo(0, -adjustY * 0.01, 0, config)
                if i == 2:
                    adjustY += 3
                    # adjustTheta += 1
            # 第二段 走20cm
            # for i in range(step2):
            #     g_motion.moveTo(20 * 0.01, 0, 0, config)
            #     # g_motion.moveTo(0, 0, -1 * almath.TO_RAD, config)
            g_motion.moveTo(step3 * 0.01, 0, 0, config)
        else:
            g_motion.moveTo(x1 * 0.01, 0, 0, config)
        g_motion.moveTo(0, y1 * 0.01, 0, config)
        time.sleep(1)
        g_motion.moveTo(0, 0, theta1, config)
        # 记录日志
        logging.info("---------------------move------------------")
        if x != 0.0:
            logging.info("X:::: " + str(x2) + "cm")
        elif y != 0.0:
            logging.info("Y::::" + str(y1) + "cm")
        else:
            logging.info("Z:::: " + str(theta) + "度")
    except Exception, e:
        logging.error("传入参数不合法！")


def rest():
    # 坐着休息
    global g_motion, g_posture
    g_motion.moveInit()
    g_motion.angleInterpolationWithSpeed("LWristYaw", math.radians(-100), 0.5)
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", math.radians(15), 0.5)
    # g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.77, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", math.radians(-10), 0.5)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", math.radians(95), 0.5)  # 7-20 改90
    g_motion.angleInterpolationWithSpeed("LElbowYaw", math.radians(20), 0.5)
    g_motion.angleInterpolationWithSpeed("RWristYaw", math.radians(100), 0.5)
    g_motion.angleInterpolationWithSpeed("RShoulderPitch", math.radians(95), 0.5)  # 7-20 改
    g_motion.angleInterpolationWithSpeed("RShoulderRoll", math.radians(-15), 0.5)
    g_motion.angleInterpolationWithSpeed("RElbowRoll", math.radians(10), 0.5)
    g_motion.angleInterpolationWithSpeed("RElbowYaw", math.radians(-20), 0.5)

    # 拿杆
    # g_motion.angleInterpolationWithSpeed("LHand", 1.0, 0.2)
    # time.sleep(4)
    # if g_memory.getData("HandRightRightTouched"):
    # g_motion.angleInterpolationWithSpeed("LHand", 0.15, 0.2)
    g_motion.setStiffnesses("LHand", 1.0)
    g_motion.setStiffnesses("LWristYaw", 1.0)
    g_motion.setStiffnesses("LShoulderPitch", 1.0)
    g_motion.setStiffnesses("LShoulderRoll", 1.0)
    g_motion.setStiffnesses("LElbowRoll", 1.0)
    g_motion.setStiffnesses("LElbowYaw", 1.0)

    g_motion.setStiffnesses("RHand", 1.0)
    g_motion.setStiffnesses("RWristYaw", 1.0)
    g_motion.setStiffnesses("RShoulderPitch", 1.0)
    g_motion.setStiffnesses("RShoulderRoll", 1.0)
    g_motion.setStiffnesses("RElbowRoll", 1.0)
    g_motion.setStiffnesses("RElbowYaw", 1.0)
    g_motion.setMoveArmsEnabled(False, False)


def ori_move():
    nao_init("NAOTwo", IP)
    rest()
    # g_posture.goToPosture("StandInit", 0.5)
    Utils.listen_tcp()
    Utils.say('receive robot one\'s massage')
    # g_motion.moveInit()
    # time.sleep(1)
    # move(15, 0, 0, config=WalkConfig.g_moveConfig6)


def start():
    ori_move()
    try:
        move_line(WalkConfig.RUN_COUNT)  # 步长
    except Exception, e:
        print e
        exit(5)
    finally:
        pass
