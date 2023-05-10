import serial

# 创建一个串口对象
ser = serial.Serial('COM2', 38400)

while True:
    # 从串口读取数据
    data = ser.readline()

    # 打印读取到的数据
    print('Received:', data)

    # 在这里实现返回数据的逻辑
    # 例如，你可以直接将接收到的数据发送回去
    ser.write(data)
