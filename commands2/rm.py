import getopt
import os
import socket

import config
from Command import Command
from utils import find_uuid
from utils import get_running_containers
from utils import send
from utils import set_interaction


class Rm(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "rm", args)

    def handle(self):
        optlist, args = getopt.getopt(self.args, 'h', ['help'])
        set_interaction(self.soc, False)
        if len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
            self.help_page(True)
        else:
            uuid_to_remove = find_uuid(args[0])
            if not uuid_to_remove:
                send(self.soc, "Cannot find container: " + args[0], newline=True)
            elif uuid_to_remove in get_running_containers():
                send(self.soc, "Cannot remove a running container!", newline=True)
            else:
                os.remove(os.path.join("container", uuid_to_remove + '.img'))
                config.delete_record(uuid_to_remove)
                send(self.soc, uuid_to_remove + " is removed", newline=True)
