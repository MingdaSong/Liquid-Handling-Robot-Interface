# 液体处理机器人控制API

本项目是一个液体处理机器人的控制API，用于控制液体处理机器人的各种操作，如初始化、吸液、排液、液面探测等。API可以通过HTTP请求进行调用。

目前已经将该服务部署到我个人的linux Ubuntu服务器上

## 技术栈

- Python
- Flask
- PySerial

## 准备工作

在运行API之前，需要完成以下准备工作：

- 安装Python 3.x
- 安装PySerial库
- 配置液体处理机器人串口连接,本处使用了模拟串口

## 配置液体处理机器人串口连接

在连接液体处理机器人之前，需要先检查液体处理机器人的串口连接情况。在本项目中，假设液体处理机器人通过串口连接到计算机，并且串口连接的端口号为COM1（Windows系统）或/dev/ttyUSB0（Linux系统）。

若连接的串口端口不是COM1或/dev/ttyUSB0，需要在`LiquidHandler`类的初始化方法中修改端口号。

## 运行API

在完成上述准备工作后，即可运行API。

- 在命令行中进入项目根目录
- 运行以下命令启动API：

  ```
  python app.py
  ```

  API将会在本地的5000端口上运行。如果要在其他主机上访问API，需要将API绑定到0.0.0.0（即所有IP地址）：

  ```
  python app.py --host 0.0.0.0
  ```

  这样API就可以通过网络IP地址进行访问。

## 调用API

API可以通过HTTP请求进行调用。以下是API端点和请求参数的说明：

- `/initialize`

  初始化液体处理机器人，设置运行速度、运行功率和TIP头。
  请求方法：POST

  请求参数：

  - `speed`（可选）：初始化时设定的运行速度（默认值为16000微步每秒）。
  - `power`（可选）：初始化时设定的运行功率（默认值为100%）。
  - `tip_head`（可选）：初始化过程中无论是否检测到TIP头都将顶出TIP（默认值为0，表示无TIP头）。
- `/detect`

  液面探测

  请求方法：POST

  请求参数：

  - `auto_report`（必须）：探测到液面后自动上报状态，设置为1。
  - `timeout`（可选）：探测超时时间，单位为毫秒（默认值为5000）。
- `/absorb`

  吸液

  请求方法：POST

  请求参数：

  - `volume`（可选）：吸液体积（默认值为10000微升）。
  - `speed`（可选）：吸液过程中运行速度（默认值为200微升每秒）。
  - `cutoff_speed`（可选）：吸液截流速度（默认值为10微升每秒）。
- `/dispense`

  排液

  请求方法：POST

  请求参数：

  - `volume`（可选）：排液体积（默认值为1000微升）。
  - `back_suck_volume`（可选）：回吸体积（默认值为500微升）。
  - `speed`（可选）：排液过程中运行速度（默认值为200微升每秒）。
  - `cutoff_speed`（可选）：排液截流速度（默认值为10微升每秒）。
- `/status`

  查询当前状态

  请求方法：GET

  请求参数：

  - 无参数
- `/read_parameter`

  读取指定参数的值

  请求方法：POST

  请求参数：

  - `parameter_number`（必须）：寄存器地址。例如，当`parameter_number`等于3时，表示查看是否有TIP头。

  `/set_parameter`

  设置指定参数的值

  请求方法：POST

  请求参数：

  - `parameter_number`（必须）：寄存器地址。例如，当`parameter_number`等于54时，表示设置液面探测系数。
  - `value`（必须）：要设置的值。例如，当`value`等于10时，表示液面探测系数设置为10。

以上所有API请求的成功回应为设备地址和执行成功状态，例如`1<2`表示目标设备地址1，指令执行成功状态2。

## 测试方法

### 1. 通过ssh登录到linux服务器并使用clinet脚本进行

```python
python client.py --url http://127.0.0.1:5000 --token your_token_here --path initialize --speed 15000 --power 100 --tip_head 0
python client.py --url http://127.0.0.1:5000 --token your_token_here --path absorb --volume 10000 --speed 200 --cutoff_speed 10
python client.py --url http://127.0.0.1:5000 --token your_token_here --path dispense --volume 1000 --back_suck_volume 500 --speed 200 --cutoff_speed 100
python client.py --url http://127.0.0.1:5000 --token your_token_here --path detect --auto_report_status 1 --timeout 5000
python client.py --url http://127.0.0.1:5000 --token your_token_here --path status
python client.py --url http://127.0.0.1:5000 --token your_token_here --path read_parameter --parameter_number 3
python client.py --url http://127.0.0.1:5000 --token your_token_here --path set_parameter --parameter_number 54 --value 10
```

### 2. 通过curl 方法进行外部访问

```python
curl -X POST [API_URL]/initialize -H "Authorization: Bearer [VALID_TOKEN]" -d "speed=16000&power=100&tip_head=0"

```
