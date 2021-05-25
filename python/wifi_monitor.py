#!/usr/bin/python
import Queue
import threading
import time
import socket

    #    A thread for monitoring UDP communication port. The port is
    #    opened when the thread is started.

    #    data_q:
    #        Queue for received data. Items in the queue are (data, timestamp) pairs,
    #        where data is a string representing the received data,
    #        and timestamp is the time elapsed from the thread's start (in seconds).

    #    error_q:
    #        Queue for error messages. If the
    #        UDP port fails to open for some reason, an error
    #        is placed into this queue.

    #    port:
    #        The UDP port to open. Must be recognized by the
    #        system.

    #    port_timeout:
    #        The timeout used for reading the UDP port. If this
    #        value is low, the thread will return data in finer
    #        grained chunks, with more accurate timestamps, but
    #        it will also consume more CPU.


class WifiMonitorThread(threading.Thread):

    def __init__(   self,
                    data_q,error_q,
                    UDP_IP,UDP_PORT,UDP_timeout=1.0):#,port_stopbits=serial.STOPBITS_ONE,port_parity=serial.PARITY_NONE):

        threading.Thread.__init__(self)

        self.data_q = data_q
        self.error_q = error_q

        self.UDP = None
        #self.UDP_arg = dict(IP=UDP_IP,port=UDP_PORT,timeout=UDP_timeout)#stopbits=port_stopbits,parity=port_parity,
        self.IP = UDP_IP
        self.UDP_port = UDP_PORT
        self.alive = threading.Event()
        self.alive.set()

    def run(self):

        try:
            if self.UDP:
                self.UDP.close()
            self.UDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.UDP.bind((self.IP,self.UDP_port))
        except socket.error , e:
            self.error_q.put("ERROR "+str(e[0])+": "+e[1])
            return


        # Restart the clock
        start_time = time.time()

        while self.alive.isSet():
            data , addr = self.UDP.recvfrom(1024)
            if len(data) > 0:
                timestamp = time.time() - start_time
                self.data_q.put((data, timestamp))

        # clean up
        if self.UDP:
            self.UDP.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)
