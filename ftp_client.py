import socket
import sys
import time

# 具体功能
class FtpClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")#发送请求
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #接收文件列表
            fs = self.sockfd.recv(4096).decode()
            print(fs)
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self):
        filename = input("请输入要下载的文件名:")
        self.sockfd.send(('G '+filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            fd = open(filename,'wb')
            #接收内容写入文件
            while True:
                content = self.sockfd.recv(1024)
                if content==b'##':
                    break
                fd.write(content)
            fd.close()
        else:
            print(data)

    def do_put(self):
        filename = input("请输入要上传的文件名:")
        try:
            fd = open(filename,'rb')
        except Exception:
            print("File not exist")
            return

        filename = filename.split('/')[-1]
        self.sockfd.send(('P '+filename).encode())
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #上传文件内容
            while True:
                content = fd.read(1024)
                if not content:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(content)
            fd.close()

# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)

    while True:
        print("-------------Menu-------------")
        print("1. file list")
        print("2. get file")
        print("3. put file")
        print("4. quit")
        print("------------------------------")

        cmd = int(input('Input command:'))
        if 1 == cmd:
            ftp.do_list()
        elif 2 == cmd:
            ftp.do_get()
        elif 3 == cmd:
            ftp.do_put()
        elif 4 == cmd:
            ftp.do_quit()


# 网络连接
def main():
    # 服务器地址
    ADDR = ('127.0.0.1', 8080)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接服务器失败")
        return
    else:
        print("""
                 ***************************
                    Data    File    Image
                 ***************************
        """)
        cls = input("Input File Dir Name:")
        if cls not in ['Data', 'File', 'Image']:
            print("Sorry! Input Error!")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)  # 发送具体的请求


if __name__ == "__main__":
    main()
