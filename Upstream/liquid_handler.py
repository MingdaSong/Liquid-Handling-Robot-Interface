import serial
import time


class LiquidHandler:
    def __init__(self, port, address, baudrate=38400):
        # 初始化串口和地址
        self.ser = serial.Serial(port, baudrate)
        self.address = address

    def send_cmd(self, cmd):
        # 在命令的末尾添加回车符并发送命令
        self.ser.write(f'{self.address}>{cmd}\n'.encode())

        # 等待一段时间让设备响应
        # time.sleep(0.1)

        # 读取返回的数据
        # result = self.ser.read(self.ser.inWaiting()).decode().strip()
        result = self.ser.read(self.ser.inWaiting()).decode()
        print(result)
        return result

    def initialize(self, speed=16000, power=100, tip_head=0):
        '''
        初始化 ADP，设置运行速度、运行功率和 TIP 头
        :param speed: 运行速度,初始化为16000微步每秒
        :param power: 运行功率,初始化为100%
        :param tip_head: 初始化过程中无论是否检测到 TIP 头都将顶出 TIP
        :return: 串口指令数据
        '''
        # 发送命令
        return self.send_cmd(f'It{speed},{power},{tip_head}')

    def detect_liquid(self, auto_report_status=1, timeout=5000):
        '''
        液面探测
        :param auto_report_status: 探测到液面后自动上报状态，默认为 1
        :param timeout: 探测超时时间，默认为 5000 毫秒
        :return: 串口指令数据
        '''
        # 发送命令
        return self.send_cmd(f'Ld{auto_report_status},{timeout}')

    def absorb(self, volume=10000, speed=200, cutoff_speed=10):
        '''
        吸液
        :param volume: 吸液体积，默认为 10000 微升
        :param speed: 吸液过程中运行速度，默认为 200 微升每秒
        :param cutoff_speed: 吸液截流速度，默认为 10 微升每秒
        :return: 串口指令数据
        '''
        # 发送命令
        return self.send_cmd(f'Ia{volume},{speed},{cutoff_speed}')

    def dispense(self, volume=1000, back_suck_volume=500, speed=200, cutoff_speed=100):
        '''
        排液
        :param volume: 排液体积，默认为 1000 微升
        :param back_suck_volume: 回吸体积，默认为 500 微升
        :param speed: 排液过程中运行速度，默认为 200 微升每秒
        :param cutoff_speed: 排液截流速度，默认为 100 微升每秒
        :return: 串口指令数据
        '''
        # 发送命令
        return self.send_cmd(f'Da{volume},{back_suck_volume},{speed},{cutoff_speed}')

    def get_status(self):
        """
        查询当前状态
        :return: 返回查询结果字符串
        """
        return self.send_cmd(f'?')

    def read_parameter(self, parameter_number):
        """
        读取指定参数的值
        :param parameter_number: 参数的编号
        :return: 返回读取结果字符串
        """
        return self.send_cmd(f'Rr{parameter_number}')

    def set_parameter(self, parameter_number, value):
        """
        设置指定参数的值
        :param parameter_number: 参数的编号
        :param value: 要设置的参数值
        :return: 返回设置结果字符串
        """
        return self.send_cmd(f'Wr{parameter_number},{value}')
