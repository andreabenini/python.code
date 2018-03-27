#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import zmq
from datetime import datetime, timedelta
from zmq.eventloop.ioloop import IOLoop, PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream
from zmq_msg_helo import *


class AppServer(object):
    def __init__(self):
        self.listen = "127.0.0.1"
        self.port = 5556
        self.ctx = zmq.Context()
        self.loop = IOLoop.instance()
        self.client_identities = {}
        self.server = self.ctx.socket(zmq.ROUTER)
        self.server.setsockopt(zmq.LINGER, 0)       # Without linger and timeouts you might have problems when closing context
        self.server.setsockopt(zmq.RCVTIMEO, 5000)  # 5s
        self.server.setsockopt(zmq.SNDTIMEO, 5000)
        bind_addr = "tcp://%s:%s" % (self.listen, self.port)
        self.server.bind(bind_addr)
        print("Server listening for new client connections at", bind_addr)
        self.server = ZMQStream(self.server)
        self.server.on_recv(self.on_recv)
        self.periodic = PeriodicCallback(self.periodictask, 1000)


    def start(self):
        self.periodic.start()
        try:
            self.loop.start()
        except KeyboardInterrupt:
            self.periodic.stop()
            print("\nClosing socket and context\n")
            self.server.close()
            self.ctx.term()


    def periodictask(self):
        stale_clients = []
        for client_id, last_seen in self.client_identities.items():
            if last_seen + timedelta(seconds=10) < datetime.utcnow():
                stale_clients.append(client_id)
            else:
                msg = HelloMessage()
                msg.send(self.server, client_id)
        for client_id in stale_clients:
            print("\nHaven't received a HELO from client %s recently. Dropping from list of connected clients." % client_id)
            del self.client_identities[client_id]
        sys.stdout.write(".")
        sys.stdout.flush()


    def on_recv(self, msg):
        identity = msg[0]
        self.client_identities[identity] = datetime.utcnow()
        msg_type = msg[1]
        print("Received message of type %s from client ID %s!" % (msg_type, identity))


if __name__ == '__main__':
    my_server = AppServer()
    my_server.start()
