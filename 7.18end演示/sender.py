import socket
import struct
import os
import json
from message_header import MessageGenerate
from datetime import datetime


def send_message(json_file_path, host, port):
    # 读取 JSON 文件内容
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Construct the desired JSON structure
    new_json = {
        "systemTypeID": 0x42,
        "systemIP": ip_address,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data":json_data
    }

    new_json_string = json.dumps(new_json, indent=4)
    #
    # print(new_json_string)
    print(32+len(new_json_string))

    # 生成message
    message = MessageGenerate(version=0x01, main_command=0x42, sub_command=0x0001, encryption_mode=0x00,
                          authentication_mode=0x00, reserved=0x0000, message_number=0x00000000, data_length=32+len(new_json_string),data=new_json_string, hashcode=0)

    # Serialize the message instance to bytes
    message_bytes = message.to_bytes()
    print(message_bytes)

    # 创建 Socket 连接
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # 发送报文数据长度和报文数据
    client_socket.sendall(message_bytes)

    # 关闭 Socket 连接
    client_socket.close()


# 示例使用

# 定义 JSON 文件路径
json_file_path = "result.json"
# file_length = 32+os.path.getsize(json_file_path)
# print(file_length)

with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 定义服务器的主机和端口
host = '192.168.43.243'
port = 50004
# host = '127.0.0.1'
# port = 10010
# 发送message
send_message(json_file_path, host, port)
# for i in range(1, 6):
#     send_message(json_file_path, host, port)
#     print("success!",i)



