import socket

def start_server(host, port):
    """
    启动TCP服务器

    :param host: 服务器主机名
    :param port: 服务器端口
    """
    # 创建一个socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定到指定的主机和端口
    s.bind((host, port))

    # 开始监听连接
    s.listen(1)

    print("Server is listening on {}:{}".format(host, port))

    while True:
        # 接受一个连接
        conn, addr = s.accept()
        print('Connected by', addr)

        while True:
            # 读取数据
            data = conn.recv(1024)
            if not data:
                break
            print('Received data:', data)

            # 在这里我们将响应数据发送回客户端
            response = "Server response: your data has been received."
            conn.sendall(response.encode())

        # 关闭连接
        conn.close()

# 使用localhost和8888端口启动服务器
start_server('localhost', 8888)
