import serial
import time


class LiquidHandler:
    def __init__(self, port, address, baudrate=38400):
        self.ser = serial.Serial(port, baudrate)
        self.address = address

    def send_cmd(self, cmd):
        # 在命令的末尾添加回车符
        self.ser.write(f'{self.address}>{cmd}\n'.encode())

        # 等待一段时间让设备响应
        time.sleep(0.1)

        # 读取返回的数据
        result = self.ser.read(self.ser.inWaiting()).decode()
        return result

    def initialize(self, speed=16000, power=100, tip_head=0):
        '''

        :param speed: 运行速度,初始化为16000微步每秒
        :param power: 运行功率,初始化为100%
        :param tip_head: 初始化过程中无论是否检测到 TIP 头都将顶出 TIP
        :return: 串口指令数据
        '''
        return self.send_cmd(f'It{speed},{power},{tip_head}')

    def detect_liquid(self, auto_report_status=1, timeout=5000):
        return self.send_cmd(f'Ld{auto_report_status},{timeout}')

    def absorb(self, volume=10000, speed=200, cutoff_speed=10):
        return self.send_cmd(f'Ia{volume},{speed},{cutoff_speed}')

    def dispense(self, volume=1000, back_suck_volume=500, speed=200, cutoff_speed=100):
        return self.send_cmd(f'Da{volume},{back_suck_volume},{speed},{cutoff_speed}')

    def get_status(self):
        return self.send_cmd(f'>?')

    def read_parameter(self, parameter_number):
        return self.send_cmd(f'>Rr{parameter_number}')

    def set_parameter(self, parameter_number, value):
        return self.send_cmd(f'>Wr{parameter_number},{value}')
