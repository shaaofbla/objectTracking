import unittest
import socket
import multiprocessing
from TCP.client import client

class TCPTestServer:
    def __init__(self, ip, port=5005, buffer_size=60):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size

    def start(self):
        print "starting server"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)
        print "where iam stuck"
        conn, addr = s.accept()
        while True:
            print "looping"
            data = conn.recv(self.buffer_size)
            if not data:
                break
            conn.send("testServer: OK")
        conn.close()
        return


class TestTCPclient(unittest.TestCase):
    default_tcp_client = client()
    tcp_client = client(ip = '192.168.0.50',port=3000, buffer_size = 100)
    tcp_testClient = client(ip='127.0.0.1')
    tcp_testServer  = TCPTestServer('127.0.0.1')

    def test_init_default_ip(self):
        self.assertEqual(self.default_tcp_client.ip, '192.168.0.11')

    def test_init_default_port(self):
        self.assertEqual(self.default_tcp_client.port, 5005)

    def test_init_default_buffer_size(self):
        self.assertEqual(self.default_tcp_client.buffer_size,60)

    def test_init_ip(self):
        self.assertEqual(self.tcp_client.ip, '192.168.0.50')

    def test_init_port(self):
        self.assertEqual(self.tcp_client.port, 3000)

    def test_init_buffer_size(self):
        self.assertEqual(self.tcp_client.buffer_size, 100)

    def test_tcp_socket(self):
        self.assertRaises(Exception,self.tcp_client.connect())

    """
    def test_tcp_test_server(self):
        clientThread = multiprocessing.Process(target=self.tcp_client.connect())
        clientThread.start()
        print "threading is working"
        self.tcp_testServer.start()
        print "sucessfully detached"
        self.tcp_client.connect()
        self.tcp_client.send("test")
        data = self.tcp_client.socket.recv(self.tcp_client.buffer_size)
        self.assertEqual(data, "testServe: OK")
    """


if __name__ == '__main__':
    unittest.main()
