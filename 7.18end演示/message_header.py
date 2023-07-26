import struct
import os
import json
import socket

class MessageGenerate:
    def __init__(self, version, main_command, sub_command, encryption_mode, authentication_mode, reserved,
                 message_number, data_length, data, hashcode):
        self.version = version
        self.main_command = main_command
        self.sub_command = sub_command
        self.encryption_mode = encryption_mode
        self.authentication_mode = authentication_mode
        self.reserved = reserved
        self.message_number = message_number
        self.data_length = data_length
        self.data = data
        self.hashcode = hashcode

    def to_bytes(self):
        header = struct.pack('!BBHBBHII', self.version, self.main_command, self.sub_command,
                             self.encryption_mode, self.authentication_mode, self.reserved,
                             self.message_number, self.data_length)
        encoded_data = self.data.encode('utf-8')  # Encode the data as bytes
        hashcode_bytes = self.hashcode.to_bytes(16, 'big')

        return header + encoded_data + hashcode_bytes

    @classmethod
    def from_bytes(cls, message_bytes):
        version, main_command, sub_command, encryption_mode, authentication_mode, \
        reserved, message_number, data_length = struct.unpack('!BBHBBHII', message_bytes[:16])
        data = message_bytes[16:data_length - 16].decode('utf-8')  # Decode the data from bytes to string
        hashcode = message_bytes[data_length - 16:]
        return cls(version, main_command, sub_command, encryption_mode, authentication_mode,
                   reserved, message_number, data_length, data, hashcode)

# # 示例使用
# file_path = "../examples/res/video_processing_report.json"
# file_length = os.path.getsize(file_path)
#
# with open(file_path, 'r') as file:
#     json_data = json.load(file)
#
# # 将报文数据转换为 JSON 字符串
# report_json = json.dumps(json_data)
#
# message = MessageGenerate(version=0x01, main_command=0x10, sub_command=0x8002, encryption_mode=0x00,
#                           authentication_mode=0x01, reserved=0x1234, message_number=0x12345678, data_length=file_length,data=report_json, hashcode=None)
#
# # 将消息转换为字节流
# message_bytes = message.to_bytes()
# print(message_bytes)
#
# # # 从字节流中恢复消息对象
# # restored_message = MessageGenerate.from_bytes(message_bytes)
# # print(restored_message.data)
# # print(restored_message.message_number)
# # print(restored_message.sub_command)
# def from_bytes(report_message):
#     return None