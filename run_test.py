import os
import socket
import unittest
from time import sleep

import run


class TestRun(unittest.TestCase):
    def setUp(self) -> None:
        if not os.path.exists('container'):
            os.mkdir('container')

    # def test_ubuntu_shell(self):
    #     run.run(False, cmd='/bin/bash')

    def test_nginx(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO nginx does not listen on IPv6
        run.run(True, cmd=('/usr/sbin/nginx', '-g', 'daemon off;'), image='nginx.img', uuid='001')
        sleep(1)
        result = soc.connect_ex(('localhost', 80))
        soc.close()
        run.terminate('001')
        self.assertEqual(result, 0, msg="Could not connect to localhost:80, return code is {0}".format(result))
        print("Nginx is running normally")


if __name__ == '__main__':
    unittest.main()
