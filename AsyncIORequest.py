#_author: Administrator
#date: 2018/4/21

import socket
import select

class HttpRequest(object):
    def __init__(self,sk,host):
        self.socket = sk
        self.host = host
    def fileno(self):
        return self.socket.fileno()


class AsyncRequest(object):
    conn =[]
    connection = []

    def add_request(self,host):
        try:
            sk = socket.socket()
            sk.setblocking(0)
            sk.connect((host,80))

        except BlockingIOError as e :
            pass
        request = HttpRequest(sk,host)
        self.conn.append(request)
        self.connection.append(request)

    def run(self):

        while True:
            rlist,wlist,elist = select.select(self.conn,self.connection,self.connection,0.02)
            for w in wlist:
                tpl = 'GET / HTTP/1.0\r\nHost:%s\r\n\r\n'%w.host
                print(w.host,'success to link')
                w.socket.send(bytes(tpl,encoding='utf-8'))
                self.connection.remove(w)
            for r in rlist:
                recv_data = bytes()
                while True:
                    try:
                        data = r.socket.recv(8096)
                        recv_data += data
                    except Exception as e:
                        break
                print(r.host,recv_data)

                self.conn.remove(r)
            if not self.connection and not self.conn:
                break

host_list = [
    'www.baidu.com',
    'cn.bing.com',
    'www.cnblog.com'
]

req = AsyncRequest()

for host in host_list:
    req.add_request(host)

req.run()