#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# TCP Daemon
#

# Program imports
import sys
import socket
import select
import multiprocessing

# Main (and only) class
class SimpleDaemon:
    def __init__(self, host, port):
        # local properties
        self._debug = True
        # TCP
        self._host = host
        self._port = port
        self._tcpTimeout = 60
        self._tcpBufferSize = 1024
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(10)   # Incoming connection limit (pretty low, local usage only)

    # Program main loop
    def loop(self):
        while True:             # until self._socketClose(self._sock)
            DataInput,_,_ = select.select([self._sock], [], [], self._tcpTimeout)
            for Input in DataInput:
                if Input is self._sock:
                    try:
                        Client, Address = self._sock.accept()
                        Client.settimeout(self._tcpTimeout)     # Client inactivity timeout (1min)
                        multiprocessing.Process(target=self._spawnClient, args=(Client, Address)).start()
                    except OSError:                             # Daemon socket close (shutdown request)
                        return

    # Close an opened socket
    def _socketClose(self, tcpSocket):
        tcpSocket.shutdown(socket.SHUT_RDWR)
        tcpSocket.close()

    # Fork client connection in a new process
    def _spawnClient(self, client, address):
        if self._debug:
            print("Client connected: {}, {}".format(client, address))
        client.settimeout(self._tcpTimeout)
        try:
            command = client.recv(self._tcpBufferSize).decode('UTF-8').rstrip()
            if command == 'shutdown':
                if self._debug:
                    print("Daemon shutdown requested, closing application")
                self._socketClose(self._sock)
                self._socketClose(client)
                return
            client.send((command+'\n').encode('UTF-8'))
        except socket.timeout:
            if self._debug:
                print("Client timeout, disconnecting {}".format(address))
        self._socketClose(client)


if __name__ == '__main__':
    try:
        daemon = SimpleDaemon('127.0.0.1', 6666)
        daemon.loop()
    except KeyboardInterrupt:
        print("\nInterrupt request, program aborted\n")
