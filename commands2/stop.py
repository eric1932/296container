import getopt
import socket

import run
from Command import Command
from utils import send
from utils import set_interaction


class Stop(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "stop", args)

    def handle(self):
        optlist, args = getopt.getopt(self.args, 'h', ['help'])
        print("DEBUG/optlist:", optlist)
        print("DEBUG/args:", args)
        set_interaction(self.soc, False)
        if len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
            self.help_page(True)
        else:
            send(self.soc, run.terminate(args[0]), newline=True)
