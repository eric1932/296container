import getopt
import os
import socket

from Command import Command
from utils import get_entry_point
from utils import send
from utils import send_arg
from utils import set_interaction
from run import run


class Run(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "run", args)

    def handle(self):
        optlist, args = getopt.getopt(self.args, 'hd', ['help'])
        print("DEBUG/optlist:", optlist)
        print("DEBUG/args:", args)
        if len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
            set_interaction(self.soc, False)
            self.help_page(True)
        elif len(args) >= 1:
            if not os.path.exists(os.path.join("base_images", args[0] + ".img")):
                # option 1: don't run
                # set_interaction(self.soc, False)
                # return
                # option 2: set default
                args[0] = "ubuntu"
            if ('-d', '') in optlist:
                set_interaction(self.soc, False)
                uuid = run(True, image=args[0],
                           cmd='/bin/uname -a' if len(args) >= 2 and args[1] == "release"
                           else (" ".join(args[1:]) if len(args) >= 2
                                 else get_entry_point(args[0])))
                send(self.soc, uuid + " started", newline=True)
            else:
                set_interaction(self.soc, True)
                # send_arg(self.soc, "detach", ("1" if ('-d', '') in optlist else "0"))
                send_arg(self.soc, "detach", "0")
                send_arg(self.soc, "image", args[0])
                # uuid should be none
                # load should be false
                send_arg(self.soc, "cmd",
                         '/bin/uname -a' if len(args) >= 2 and args[1] == "release"
                         else (" ".join(args[1:]) if len(args) >= 2
                               else get_entry_point(args[0])))
                send(self.soc, "next")  # end of passing args
        # elif len(args) == 2:
        #     uuid = find_uuid(args[0])
        #     if uuid:
        #         set_interaction(self.soc, True)
        #         send_arg(self.soc, "uuid", uuid)
        #         send_arg(self.soc, "load", "1")
        #         send(self.soc, "next")  # end of passing args
        #     else:
        #         set_interaction(self.soc, False)
        #         send(self.soc, "No matching uuid found!", newline=True)
        # else:
        #     pass