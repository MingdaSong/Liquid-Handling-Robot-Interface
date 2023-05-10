import serial
import time


class LiquidHandler:
    def __init__(self, port, baudrate=38400):
        self.ser = serial.Serial(port, baudrate)

    def send_cmd(self, cmd):
        # 在命令的末尾添加回车符
        self.ser.write((cmd + '\n').encode())

        # 等待一段时间让设备响应
        time.sleep(0.1)

        # 读取返回的数据
        result = self.ser.read(self.ser.inWaiting()).decode()
        return result

    def initialize(self, speed=16000, power=100, tip_head=0):
        return self.send_cmd(f'1>It{speed},{power},{tip_head}')

    def detect_liquid(self, auto_report_status=1, timeout=5000):
        return self.send_cmd(f'1>Ld{auto_report_status},{timeout}')

    def aspirate(self, volume=10000, speed=200, cutoff_speed=10):
        return self.send_cmd(f'1>Ia{volume},{speed},{cutoff_speed}')

    def dispense(self, volume=1000, back_suck_volume=500, speed=200, cutoff_speed=100):
        return self.send_cmd(f'1>Da{volume},{back_suck_volume},{speed},{cutoff_speed}')

    def get_status(self):
        return self.send_cmd('1>?')

    def read_parameter(self, parameter_number):
        return self.send_cmd(f'1>Rr{parameter_number}')

    def set_parameter(self, parameter_number, value):
        return self.send_cmd(f'1>Wr{parameter_number},{value}')
