import requests
import json

url = "http://127.0.0.1:5000/initialize"  # 你的 Flask 应用的 URL

# 你的 POST 数据
data = {
    "speed": "16000",
    "power": "100",
    "tip_head": "0"
}

# 你的请求头，包含了 token
headers = {
    "token": "your_token_here"
}

# 发送 POST 请求
response = requests.post(url, json=data, headers=headers)

# 打印响应
print(response.json())
print("Status code:", response.status_code)
print("Response body:", response.text)
