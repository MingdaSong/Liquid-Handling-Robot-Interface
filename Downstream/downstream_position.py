import time
import serial

ser = serial.Serial('/dev/pts/6', 38400)

while True:
    # 从串口读取数据
    data = ser.readline()
    # 将数据转换为字符串
    data_str = data.decode().strip()

    # 解析数据
    if len(data_str) > 0:
        idx = data_str.find('>')

        # 如果找不到">"，那么数据是无效的，返回 "invalid data"
        if idx == -1:
            ser.write('invalid data\n'.encode())
        else:
            # 取">"前面的所有字符作为地址，方向为">"后面的第一个字符，剩下的是数据
            addr = data_str[:idx]
            direction = data_str[idx]
            data = data_str[idx + 1:]

            print('command:', data_str)
            print(f'addr: {addr}, direction: {direction}, data: {data}')

            # 根据不同的数据类型，返回不同的状态码
            if data[:2] == 'It':
                ser.write((f'{addr}<2\n').encode())
            elif data[:2] == 'Ld':
                ser.write((f'{addr}<4\n').encode())
            elif data[:2] == 'Ia':
                ser.write((f'{addr}<2\n').encode())
            elif data[:2] == 'Da':
                ser.write((f'{addr}<2\n').encode())
            elif data[0] == '?':
                # print(1)
                ser.write((f'{addr}<0\n').encode())
            elif data[:2] == 'Rr':
                ser.write((f'{addr}<2:0\n').encode())
            elif data[:2] == 'Wr':
                ser.write((f'{addr}<2\n').encode())

    else:
        print('Received:', data_str)


