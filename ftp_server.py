"""
ftp 文件服务器
并发网络功能训练
"""

import socket
import os, sys
import threading
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8080
ADDR = (HOST, PORT)
FTP = './'  # 文件库路径


# 将客户端请求功能封装为类
class FtpServer:
    def __init__(self, connfd, ftp_path):
        self.connfd = connfd
        self.path = ftp_path

    def do_list(self):
        # 获取文件信息
        files = os.listdir(self.path)
        if not files:
            self.connfd.send("this dir is empty".encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)

            # 过滤隐藏文件
            fs = ''
            for file in files:
                if file[0] != '.' and os.path.isfile(self.path + file):
                    fs += file + '\n'#人为添加消息边界(\n)，防止粘包问题
            self.connfd.send(fs.encode())

    def do_get(self,filename):
        #下载文件
        try:
            fd = open(self.path+filename,'rb')
        except Exception:
            self.connfd.send('File not found'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        #发送文件内容
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self,filename):
        if os.path.exists(self.path+filename):
            self.connfd.send('this file has existed'.encode())
            return

        self.connfd.send(b'OK')
        fd = open(self.path + filename, 'wb')
        # 开始接收文件内容
        while True:
            content = self.connfd.recv(1024)
            if content == b'##':
                break
            fd.write(content)
        fd.close()

# 客户端请求处理函数
def handle(connfd):
    cls = connfd.recv(1024).decode()
    FTP_PATH = FTP + cls + '/'
    ftp = FtpServer(connfd, FTP_PATH)
    while True:
        # 接收客户端请求
        data = connfd.recv(1024).decode()
        #如果客户端断开返回data为空
        if not data or data[0] == 'Q':
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == 'G':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0] == 'P':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)

# 网络搭建
def main():
    # 创建套接字
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 8080...")
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("退出服务端程序")
            return
        except Exception as e:
            print("服务器报错:", e)
            continue

        print("Connect client:", addr)

        # 创建线程处理请求
        client = threading.Thread(target=handle, args=(connfd,))
        client.setDaemon(True)  # 分支线程随主线程退出
        client.start()


if __name__ == "__main__":
    main()
