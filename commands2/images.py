import getopt
import os
import socket

from Command import Command
from utils import send
from utils import set_interaction


class Images(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "images", args)

    def handle(self):
        optlist, args = getopt.getopt(self.args, 'h', ['help'])
        set_interaction(self.soc, False)
        if ('--help', '') in optlist or ('-h', '') in optlist:
            self.help_page(True)
        else:
            send(self.soc, "REPOSITORY\tSIZE", newline=True)
            for file in os.listdir("base_images"):
                if file.endswith(".img"):
                    send(self.soc, file[:-4] + "\t\t" +
                         str(os.path.getsize(os.path.join("base_images", file)) / 1024 ** 2) + "MB"
                         , newline=True)
