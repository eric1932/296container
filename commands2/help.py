import os
import socket

from Command import Command
from utils import send
from utils import set_interaction


class Help(Command):
    def __init__(self, soc: socket.socket):
        super().__init__(soc, "help", [])

    def handle(self):
        set_interaction(self.soc, False)
        # with open("docs/help.txt") as f:
        #     send(self.soc, f.read(), newline=True)
        send(self.soc, "commands: ", newline=False)
        for cmd in sorted(os.listdir("commands2")):
            if not cmd.endswith(".py") or cmd == "help.py":
                continue
            send(self.soc, cmd[:-3] + " ", newline=False)
        send(self.soc, "stop-server", newline=True)  # built-in & trailing newline
