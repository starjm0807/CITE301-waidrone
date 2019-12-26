import subprocess
import socket
import threading
from threading import Thread
from multiprocessing import Process
from multiprocessing import Manager

from Packet import *


def init(d_coordinate):
    # create server
    tracking_server = Process(target=run_server, args=(d_coordinate, 'localhost', 9000))
    tracking_server.start()
    pot_server = Process(target=run_server, args=(d_coordinate, 'localhost', 9001))
    pot_server.start()

    # run odaslive program using another thread
    subprocess.call('../bin/odaslive -c ../bin/respeaker.cfg', shell=True)


# create TCP server and receive data
def run_server(d_coordinate, host='localhost', port=9000):
    def __update_coordinate(msg, d_coordinate):
        try:
            packet = Packet(msg)
            pass
        except:
            return

        coordinate = packet.max_coordinate()
        d_coordinate.value = coordinate
        # print("server : {}".format(d_coordinate.value))

    buf_size = 1024
    with socket.socket() as sock:
        # create TCP server
        sock.bind((host, port))

        # wait for mic client
        print("server listening to {0}:{1}".format(host, port))
        sock.listen()
        conn, addr = sock.accept()
        print("new client connection from {0}:{1}".format(addr[0], addr[1]))

        # receive data from the client
        # packet_num = 0
        while conn.fileno():
            # HACK: close connection if connection closed
            data = conn.recv(buf_size)
            msg = data.decode()
            if port == 9000:
                # HACK: cut msg string properly
                __update_coordinate(msg, d_coordinate)

