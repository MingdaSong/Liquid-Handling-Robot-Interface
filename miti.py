import subprocess

# 启动第一个脚本
p1 = subprocess.Popen(["python", "upstream_position.py"])

# 启动第二个脚本
p2 = subprocess.Popen(["python", "downstream_position.py"])

# 等待两个脚本都运行完成
p1.wait()
p2.wait()
