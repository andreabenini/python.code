import socket
import select
import multiprocessing

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8008))
sock.listen(10)                                  # Connections that can be queued up waiting to be accepted
Running = True
TIMEOUT = 60
while Running:
    DataInput,_,_ = select.select([sock], [], [], TIMEOUT)
    for Input in DataInput:
        if Input is sock:
            Client, Address = sock.accept()
            Client.settimeout(TIMEOUT)                                             # Client inactivity timeout (1min)
            multiprocessing.Process(target=TCP_ClientSpawn, args=(Client, Address)).start()


def TCP_ClientSpawn(self, client, address):
    Running = True
    BUFFERSIZE = 1024
    while Running:
        Command = client.recv(BUFFERSIZE).decode('UTF-8').rstrip()
        if Command == 'quit':
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            return
        if Command:                                                                 # Set the response to echo back the recieved data 
            client.send((Command+'\n').encode('UTF-8'))
        else:
            raise Exception('Client disconnected [Command:%s]' % Command)
