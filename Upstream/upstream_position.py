from flask import Flask, request, jsonify, abort
from liquid_handler import LiquidHandler

from functools import wraps
from flask import request, abort

# 配置Token，用于身份验证
VALID_TOKEN = "your_token_here"

app = Flask(__name__)

handler = LiquidHandler('/dev/pts/5', 2)


def check_token(token):
    return token == VALID_TOKEN


def validate_json_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            abort(404)
        if token != VALID_TOKEN:
            abort(401)
        data = request.get_json()
        if not data:
            abort(400, description="Invalid JSON.")
        return f(*args, **kwargs)

    return decorated


@app.route('/initialize', methods=['POST'])
@validate_json_token
def initialize():
    speed = request.json.get('speed', 16000)
    power = request.json.get('power', 100)
    tip_head = request.json.get('tip_head', 0)
    response = handler.initialize(speed, power, tip_head)
    return jsonify(response=response)


@app.route('/absorb', methods=['POST'])
@validate_json_token
def absorb():
    volume = request.json.get('volume', 10000)
    speed = request.json.get('speed', 200)
    cutoff_speed = request.json.get('cutoff_speed', 10)

    # 在此可以加入对 volume, speed, cutoff_speed 参数的校验逻辑
    response = handler.absorb(volume, speed, cutoff_speed)
    return jsonify(response=response)


@app.route('/dispense', methods=['POST'])
@validate_json_token
def dispense():
    volume = request.json.get('volume', 1000)
    back_suck_volume = request.json.get('back_suck_volume', 500)
    speed = request.json.get('speed', 200)
    cutoff_speed = request.json.get('cutoff_speed', 100)

    # 在此可以加入对 volume, back_suck_volume, speed, cutoff_speed 参数的校验逻辑
    response = handler.dispense(volume, back_suck_volume, speed, cutoff_speed)
    return jsonify(response=response)


@app.route('/detect', methods=['POST'])
@validate_json_token
def detect():
    auto_report_status = request.json.get('auto_report_status', 1)
    timeout = request.json.get('timeout', 5000)

    # 在此可以加入对 auto_report_status, timeout 参数的校验逻辑
    response = handler.detect_liquid(auto_report_status, timeout)
    return jsonify(response=response)


@app.route('/status', methods=['GET'])
def get_status():
    if not check_token(request.headers.get('token')):
        abort(401)
    response = handler.get_status()
    return jsonify(response=response)


@app.route('/read_parameter', methods=['POST'])
def read_parameter():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    parameter_number = data.get('parameter_number')
    if not parameter_number:
        abort(400, description="Invalid parameter_number.")
    response = handler.read_parameter(parameter_number)
    return jsonify(response=response)


@app.route('/set_parameter', methods=['POST'])
def set_parameter():
    if not check_token(request.headers.get('token')):
        abort(401)
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON.")
    parameter_number = data.get('parameter_number')
    value = data.get('value')
    if not parameter_number:
        abort(400, description="Invalid parameter_number.")
    if not value:
        abort(400, description="Invalid value.")
    response = handler.set_parameter(parameter_number, value)
    return jsonify(response=response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
