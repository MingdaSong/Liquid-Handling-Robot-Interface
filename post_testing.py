import requests
import json

url = "http://127.0.0.1:5000/initialize"  # 你的 Flask 应用的 URL

# 你的 POST 数据
data = {
    "speed": "16000",
    "power": "100",
    "tip_head": "0"
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印响应
print(response.json())

