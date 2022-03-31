import socket
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 2345))
s.listen(1)
print('Server Running')

while True:
    conn, addr = s.accept()
    while conn:
        try:
            msg = conn.recv(4096).decode('utf-8')
            if msg == 'listallfiles':
                reply=''
                files = os.listdir(os.curdir)
                for i in files:
                    reply = reply + str(i) + ' '
                conn.send(bytes(reply, 'utf-8'))


            elif msg.split()[0] == 'download' and msg.split()[1] == 'all':
                files = os.listdir(os.curdir)
                n = len(files)
                conn.send(str(n).encode('utf-8'))
                for i in files:
                    conn2, addr2 = s.accept()
                    file_name = i
                    conn2.send(file_name.encode('utf-8'))
                    time.sleep(0.02)
                    file_size = os.path.getsize(file_name)
                    conn2.send(str(file_size).encode('utf-8'))
                    with open(file_name, "rb") as file:
                        c = 0
                        while c <= file_size:
                            data = file.read(1024)
                            if not (data):
                                break
                            conn2.sendall(data)
                            c += len(data)
                        conn2.close()



            elif msg.split()[0] == 'download':
                file_name = msg.split()[1]
                # print('file name is ',file_name)
                file_size = os.path.getsize(file_name)
                # print('file size is',file_size)
                conn.send(str(file_size).encode('utf-8'))
                server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # print('socket opened')
                with open(file_name, "rb") as file:
                    c = 0
                    while c <= file_size:
                        data = file.read(8192)
                        if not data:
                            break
                        server.sendto(data, (socket.gethostname(), 2333))
                        time.sleep(0.002)
                        # print('data sent')
                        c += len(data)
                        # print('updated c')
                    # print('file sent')
                    server.close()

            else:
                reply = 'invalid input'
                conn.send(bytes(reply, 'utf-8'))
                # print(msg)
        except :
            conn = False







