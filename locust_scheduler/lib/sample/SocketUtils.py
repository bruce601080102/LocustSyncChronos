import socket
import time, os
from lib.sample.LocustSysUtils import LocustWebServer


class SocketUtils(LocustWebServer):
    def __init__(self, init_logger, master_ip, master_port, list_worker_ip):
        self.HOST = '127.0.0.1'
        self.PORT = 12345  
        self.BUFFER_SIZE = 4096  
        self.pwd = os.getcwd()
        self.save_path = os.getcwd() + "/scripts/"
        self.init_logger = init_logger
        self.master_host = master_ip
        self.master_port = master_port
        self.list_worker_ip = list_worker_ip
    
    def server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.HOST, self.PORT))

        while True:
            server_socket.listen(1)

            print("等待客户端连接...")
            client_socket, addr = server_socket.accept()
            print("客户端已连接:", addr)

            # 接收文件名
            filename = client_socket.recv(self.BUFFER_SIZE).decode()
            print("接收到文件名:", filename)
            time.sleep(0.1)
            # 接收文件内容并写入新文件
            with open(self.save_path + filename, 'wb') as file:
                while True:
                    data = client_socket.recv(self.BUFFER_SIZE)
                    if not data:
                        break
                    file.write(data)

            print("文件传输完成。")

            client_socket.close()
            self.run_worker(filename)

    def client(self, filename):
        for ip in self.list_worker_ip:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, self.PORT))
            client_socket.send(filename.encode())
            time.sleep(0.1)

            with open(self.save_path + filename, 'rb') as file:
                while True:
                    data = file.read(self.BUFFER_SIZE)
                    if not data:
                        break
                    client_socket.sendall(data)

            print("文件传输完成。")
            client_socket.close()
            
    def run(self):
        self.server()
        self.run_worker(self.filename)
