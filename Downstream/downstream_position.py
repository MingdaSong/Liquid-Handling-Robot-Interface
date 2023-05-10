import time
import serial

ser = serial.Serial('COM2', 38400)

count = 0
while True:
    # 从串口读取数据
    print(count)
    data = ser.readline()

    # 将数据转换为字符串
    data_str = data.decode().strip()

    # 解析数据
    if len(data_str) >= 5:

        idx = data_str.find('>')

        # 如果找不到">"，那么数据是无效的
        if idx == -1:
            print("invalid data")

        # 取">"前面的所有字符作为地址
        addr = data_str[:idx]
        direction = data_str[idx]  # 方向
        data = data_str[idx+1:]  # 数据

        print(f'Received: addr: {addr}, direction: {direction}, data: {data}')

        # 在这里实现返回数据的逻辑
        # 将状态码发送回去
        ser.write((f'{addr}<2\n').encode())
    else:
        print('Received:', data_str)

    time.sleep(1)
    count += 1
