# import serial
# import time
#
#
# class LiquidHandler:
#     def __init__(self, port, baudrate=38400):
#         self.ser = serial.Serial(port, baudrate)
#
#     def send_cmd(self, cmd):
#         # 在命令的末尾添加回车符
#         self.ser.write((cmd + '\r').encode())
#
#         # 等待一段时间让设备响应
#         time.sleep(0.1)
#
#         # 读取返回的数据
#         result = self.ser.read(self.ser.inWaiting()).decode()
#         return result
#
#     def initialize(self):
#         return self.send_cmd('1>It16000,100,0')
#
#     def detect_liquid(self):
#         return self.send_cmd('1>Ld1,5000')
#
#     def aspirate(self):
#         return self.send_cmd('1>Ia10000,200,10')
#
#     def dispense(self):
#         return self.send_cmd('1>Da1000,500,200,100')
#
#     def get_status(self):
#         return self.send_cmd('1>?')
#
#     def read_parameter(self):
#         return self.send_cmd('1>Rr3')
#
#     def set_parameter(self):
#         return self.send_cmd('1>Wr54,10')
#
#
# handler = LiquidHandler('COM1')  # 用你的串口名称替换'COM3'
# print(handler.detect_liquid())
from flask import Flask, request, jsonify, abort
import serial

# 配置你的 Token，用于身份验证
VALID_TOKEN = "your_token_here"

app = Flask(__name__)

ser = serial.Serial('COM1', 38400)


def dt_command(cmd):
    try:
        ser.write((f"1>{cmd}\n").encode())
        response = ser.readline().decode()
    except serial.SerialException as e:
        abort(500, description=str(e))
    return response


def check_token(token):
    return token == VALID_TOKEN


@app.route('/initialize', methods=['POST'])
def initialize():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    speed = data.get('speed', '16000')
    power = data.get('power', '100')
    tip_head = data.get('tip_head', '0')
    # 在此可以加入对 speed, power, tip_head 参数的校验逻辑
    response = dt_command(f"It{speed},{power},{tip_head}")
    return jsonify(response=response)


@app.route('/absorb', methods=['POST'])
def absorb():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    volume = data.get('volume', '10000')
    speed = data.get('speed', '200')
    cutoff_speed = data.get('cutoff_speed', '10')
    # 在此可以加入对 volume, speed, cutoff_speed 参数的校验逻辑
    response = dt_command(f"Ia{volume},{speed},{cutoff_speed}")
    return jsonify(response=response)


@app.route('/dispense', methods=['POST'])
def dispense():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    volume = data.get('volume', '1000')
    back_suck_volume = data.get('back_suck_volume', '500')
    speed = data.get('speed', '200')
    cutoff_speed = data.get('cutoff_speed', '100')
    # 在此可以加入对 volume, back_suck_volume, speed, cutoff_speed 参数的校验逻辑
    response = dt_command(f"Da{volume},{back_suck_volume},{speed},{cutoff_speed}")
    return jsonify(response=response)


@app.route('/detect', methods=['POST'])
def detect():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    auto_report_status = data.get('auto_report_status', '1')
    timeout = data.get('timeout', '5000')
    # 在此可以加入对 auto_report_status, timeout 参数的校验逻辑
    response = dt_command(f"Ld{auto_report_status},{timeout}")
    return jsonify(response=response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
