import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 2345))

while True:
    ip = input('')
    if ip == 'exit':
        print('exiting')
        s.close()
        exit(0)


    elif ip.split()[0] == 'download' and ip.split()[1] == 'all':
        s.send(bytes(ip, 'utf-8'))
        n = int(s.recv(1024).decode('utf-8'))
        lst=[]
        for i in range(n):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((socket.gethostname(), 2345))
            file_name = client.recv(1024).decode('utf-8')
            lst.append(file_name)
            file_size = client.recv(1024).decode('utf-8')
            with open(file_name, "wb") as file:
                size = 0
                while size <= int(file_size):
                    data = client.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    size += len(data)
                client.close()
        print('Downloaded ',end='')
        for i in lst:
            print(i,end=' ')
        print()




    elif ip.split()[0] == 'download':
        s.send(bytes(ip, 'utf-8'))
        file_name = ip.split()[1]
        # print('file name is ', file_name)
        file_size = s.recv(1024).decode('utf-8')
        # print('file size recvd: ', file_size)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           #UDP
        client.bind((socket.gethostname(), 2333))
        # print('socket opened')
        with open(file_name, "wb") as file:
            size = 0
            while size <= int(file_size):
                # print('inside while loop')
                conn = client.recv(8192)
                # print('data recvd')
                file.write(conn)
                # print('file write working')
                size += len(conn)
                # print('size updated to : ',size)
                if size == int(file_size):
                    # print('entered if size==filesize statement')
                    client.close()
                    break
        print('Downloaded', file_name)

    else:
        s.send(bytes(ip, 'utf-8'))
        msg = s.recv(1024)
        print(msg.decode('utf-8'))

