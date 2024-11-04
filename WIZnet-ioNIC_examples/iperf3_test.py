import json
import select
import socket
import struct
import sys
import time
import threading
from random import randint


# Provide a urandom() function for generating random bytes
def urandom(n):
    return bytes(randint(0, 255) for _ in range(n))


# iperf3 cookie size, last byte is null byte
COOKIE_SIZE = 37

# iperf3 commands
PARAM_EXCHANGE = 9
CREATE_STREAMS = 10
TEST_START = 1
TEST_RUNNING = 2
TEST_END = 4
EXCHANGE_RESULTS = 13
DISPLAY_RESULTS = 14
IPERF_DONE = 16


def make_cookie():
    cookie_chars = b"abcdefghijklmnopqrstuvwxyz234567"
    cookie = bytearray(COOKIE_SIZE)
    for i, x in enumerate(urandom(COOKIE_SIZE - 1)):
        cookie[i] = cookie_chars[x & 31]
    return cookie


class Stats:
    def __init__(self, param):
        self.pacing_timer_us = param["pacing_timer"] * 1000
        self.udp = param.get("udp", False)
        self.reverse = param.get("reverse", False)
        self.running = False

    def start(self):
        self.running = True
        self.t0 = self.t1 = time.time()
        self.nb0 = self.nb1 = 0  # num bytes

    def add_bytes(self, n):
        if not self.running:
            return
        self.nb0 += n
        self.nb1 += n

    def update(self, final=False):
        if not self.running:
            return
        t2 = time.time()
        dt = t2 - self.t1
        if final or dt > self.pacing_timer_us / 1e6:
            ta = self.t1 - self.t0
            tb = t2 - self.t0
            print(f" {ta:.2f}-{tb:.2f} sec  {self.nb1 / 1024:.2f} KBytes")
            self.t1 = t2
            self.nb1 = 0

    def stop(self):
        self.update(True)
        self.running = False
        t3 = time.time()
        dt = t3 - self.t0
        print("- " * 30)
        print(f"0.00-{dt:.2f} sec  {self.nb0 / 1024:.2f} KBytes  sender")


def client(host, port=5201, udp=False, reverse=False, bandwidth=10 * 1024 * 1024):
    print(
        "CLIENT MODE:", "UDP" if udp else "TCP", "receiving" if reverse else "sending"
    )

    param = {
        "client_version": "3.6",
        "omit": 0,
        "parallel": 1,
        "pacing_timer": 1000,
        "time": 10,
    }

    if udp:
        param["udp"] = True
        param["len"] = 1500 - 42
        param["bandwidth"] = bandwidth
    else:
        param["tcp"] = True
        param["len"] = 3000

    if reverse:
        param["reverse"] = True

    # Connect to server
    ai = socket.getaddrinfo(host, port)[0]
    print("Connecting to", ai[-1])
    print(f"ai={ai}")
    s_ctrl = socket.socket(ai[0], socket.SOCK_STREAM)
    s_ctrl.connect(ai[-1])

    # Send our cookie
    cookie = make_cookie()
    s_ctrl.sendall(cookie)

    # Object to gather statistics about the run
    stats = Stats(param)

    # Run the main loop, waiting for incoming commands and data
    poll = select.poll()
    poll.register(s_ctrl, select.POLLIN)
    buf = None
    s_data = None
    start = None

    while True:
        for pollable in poll.poll(1000):
            if pollable[0] == s_ctrl.fileno():
                # Receive command
                cmd = s_ctrl.recv(1)[0]
                if cmd == TEST_START:
                    if reverse:
                        # Start receiving data now, because data socket is open
                        if s_data:
                            poll.register(s_data, select.POLLIN)
                            start = time.time()
                            stats.start()
                elif cmd == TEST_RUNNING:
                    if not reverse:
                        # Start sending data now, ensure s_data is initialized
                        if s_data:
                            poll.register(s_data, select.POLLOUT)
                            start = time.time()
                            stats.start()
                elif cmd == PARAM_EXCHANGE:
                    param_j = json.dumps(param)
                    s_ctrl.sendall(struct.pack(">I", len(param_j)))
                    s_ctrl.sendall(bytes(param_j, "ascii"))
                elif cmd == CREATE_STREAMS:
                    if udp:
                        s_data = socket.socket(ai[0], socket.SOCK_DGRAM)
                        print(f'data={struct.pack("<I", 123456789)}')
                        s_data.sendto(struct.pack("<I", 123456789), ai[-1])
                        s_data.recv(4)
                    else:
                        s_data = socket.socket(ai[0], socket.SOCK_STREAM)
                        s_data.connect(ai[-1])
                        s_data.sendall(cookie)
                    buf = bytearray(urandom(param["len"]))
                elif cmd == TEST_RUNNING and s_data:
                    if not reverse:
                        # Start sending data
                        stats.start()
                        while stats.running:
                            try:
                                n = s_data.send(buf)
                                if n == 0:
                                    break
                                stats.add_bytes(n)
                                print(f"stats={stats}")
                            except socket.error as e:
                                if e.errno != 11:  # Resource temporarily unavailable
                                    stats.stop()
                                    break
                                time.sleep(0.01)  # Avoid busy loop
                    else:
                        # Start receiving data
                        stats.start()
                        while stats.running:
                            try:
                                n = s_data.recv_into(buf)
                                if n == 0:
                                    stats.stop()
                                    break  # Connection closed
                                stats.add_bytes(n)
                            except socket.error as e:
                                if e.errno != 11:  # Resource temporarily unavailable
                                    stats.stop()
                                    break
                                time.sleep(0.01)  # Avoid busy loop
                elif cmd == EXCHANGE_RESULTS:
                    if s_data:
                        poll.unregister(s_data)
                        s_data.close()
                        s_data = None

                    results = {
                        "cpu_util_total": 1,
                        "cpu_util_user": 0.5,
                        "cpu_util_system": 0.5,
                        "sender_has_retransmits": 1,
                        "congestion_used": "cubic",
                        "text": "Hi",
                        "streams": [
                            {
                                "id": 1,
                                "bytes": stats.nb0,
                                "retransmits": 0,
                                "jitter": 0,
                                "errors": 0,
                                "packets": 0,
                                "start_time": 0,
                                "end_time": time.time() - start,
                            }
                        ],
                    }
                    results = json.dumps(results)
                    print(f"results={results}")
                    s_ctrl.sendall(struct.pack(">I", len(results)))
                    s_ctrl.sendall(bytes(results, "ascii"))

                elif cmd == DISPLAY_RESULTS:
                    s_ctrl.sendall(bytes([IPERF_DONE]))
                    s_ctrl.close()
                    time.sleep(1)
                    return

            stats.update()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
        client(sys.argv[1], port=port, udp=False, reverse=False)
    else:
        client(sys.argv[1], udp=False, reverse=False)
