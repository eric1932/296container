import getopt
import socket

from Command import Command
from utils import find_uuid
from utils import send
from utils import send_arg
from utils import set_interaction


class Run(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "run", args)

    def handle(self):
        optlist, args = getopt.getopt(self.args, 'h', ['help'])
        if len(optlist) == 0 and len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
            set_interaction(self.soc, False)
            with open("docs/run.txt") as f:
                send(self.soc, f.read(), newline=True)
        elif len(args) == 1:
            set_interaction(self.soc, True)
            send(self.soc, "next")  # end of passing args
        elif len(args) == 2:
            uuid = find_uuid(args[0])
            if uuid:
                set_interaction(self.soc, True)
                send_arg(self.soc, "uuid", uuid)
                send_arg(self.soc, "load", "1")
                send(self.soc, "next")  # end of passing args
            else:
                set_interaction(self.soc, False)
                send(self.soc, "No matching uuid found!", newline=True)
        else:
            pass