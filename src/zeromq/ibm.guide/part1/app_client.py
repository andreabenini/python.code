#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zmq
from datetime import datetime, timedelta
from zmq.eventloop.ioloop    import IOLoop
from zmq.eventloop.ioloop    import PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream
from zmq_msg_helo import *


class AppClient(object):
    def __init__(self):
        self.ctx = zmq.Context()
        self.loop = IOLoop.instance()
        self.endpoint = "tcp://127.0.0.1:5556"
        self.client = self.ctx.socket(zmq.DEALER)
        self.client.setsockopt(zmq.LINGER, 0)       # Without linger and timeouts you might have problems when closing context
        self.client.setsockopt(zmq.RCVTIMEO, 5000)  # 5s
        self.client.setsockopt(zmq.SNDTIMEO, 5000)
        print("Connecting to", self.endpoint)
        self.client.connect(self.endpoint)
        self.client = ZMQStream(self.client)
        self.client.on_recv(self.on_recv)
        self.periodic = PeriodicCallback(self.periodictask, 1000)
        self.last_recv = None


    def disconnect(self):
        if self.ctx is not None:
            try:
                self.periodic.stop()
                print("Closing socket and context")
                self.client.close()
                self.ctx.term()
            except Exception as e:
                print(e)


    def periodictask(self):
        if self.client is None:
            return
        if not self.last_recv or self.last_recv + timedelta(seconds=5) < datetime.utcnow():
            print("No data from remote (5s)... [ping]")
        print("Sending HELLO to server")
        msg = HelloMessage()
        msg.send(self.client)


    def start(self):
        try:
            self.periodic.start()
            self.loop.start()
            msg = HelloMessage()
            msg.send(self.client)
        except KeyboardInterrupt:
            print("\n\nCtrl+C detected\n")
        except Exception as E:
            print("WTF ! Error detected")
            print(E)
        finally:
            self.disconnect()


    def on_recv(self, msg):
        self.last_recv = datetime.utcnow()
        print("Received a message of type %s from server!" % msg[0])


if __name__ == '__main__':
    my_client = AppClient()
    my_client.start()
