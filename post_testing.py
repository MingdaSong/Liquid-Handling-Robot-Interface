import argparse
import requests

# 解析命令行参数
parser = argparse.ArgumentParser(description='Send HTTP request to Flask API.')
parser.add_argument('--url', type=str, help='URL of the Flask API')
parser.add_argument('--token', type=str, help='Token for authentication')
parser.add_argument('--path', type=str, help='API path to be accessed')
parser.add_argument('--speed', type=int, help='Initialization speed for liquid handler')
parser.add_argument('--power', type=int, help='Initialization power for liquid handler')
parser.add_argument('--tip_head', type=int, help='Initialization tip head status for liquid handler')
parser.add_argument('--volume', type=int, help='Volume for liquid handling')
parser.add_argument('--back_suck_volume', type=int, help='Back-suck volume for liquid handling')
parser.add_argument('--cutoff_speed', type=int, help='Cutoff speed for liquid handling')
parser.add_argument('--auto_report_status', type=int, help='Auto-report status for liquid detection')
parser.add_argument('--timeout', type=int, help='Timeout for liquid detection')
parser.add_argument('--parameter_number', type=int, help='Parameter number for read/write')
parser.add_argument('--value', type=int, help='Value for parameter setting')

args = parser.parse_args()

# 构造请求头和数据
headers = {'token': args.token}
data = {}

# 处理参数
if args.speed is not None:
    data['speed'] = args.speed
if args.power is not None:
    data['power'] = args.power
if args.tip_head is not None:
    data['tip_head'] = args.tip_head
if args.volume is not None:
    data['volume'] = args.volume
if args.back_suck_volume is not None:
    data['back_suck_volume'] = args.back_suck_volume
if args.cutoff_speed is not None:
    data['cutoff_speed'] = args.cutoff_speed
if args.auto_report_status is not None:
    data['auto_report_status'] = args.auto_report_status
if args.timeout is not None:
    data['timeout'] = args.timeout
if args.parameter_number is not None:
    data['parameter_number'] = args.parameter_number
if args.value is not None:
    data['value'] = args.value

# 发送请求
if args.path == 'status':
    response = requests.get(f'{args.url}/{args.path}', headers=headers)
else:
    response = requests.post(f'{args.url}/{args.path}', headers=headers, json=data)

# 输出响应
print(response.json())
print("Status code:", response.status_code)
print("Response body:", response.text)

# 测试命令行代码


# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path initialize --speed 15000 --power 100 --tip_head 0
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path absorb --volume 10000 --speed 200 --cutoff_speed 10
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path dispense --volume 1000 --back_suck_volume 500 --speed 200 --cutoff_speed 100
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path detect --auto_report_status 1 --timeout 5000
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path status
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path read_parameter --parameter_number 3
# python post_testing.py --url http://127.0.0.1:5000 --token your_token_here --path set_parameter --parameter_number 54 --value 10
