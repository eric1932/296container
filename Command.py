import abc
import os
import socket

from utils import send
from utils import set_interaction


class Command(abc.ABC):
    def __init__(self, soc: socket.socket, cmd: str, args: list):
        self.cmd = cmd
        self.soc = soc
        self.args = args
        self.handle()

    @abc.abstractmethod
    def handle(self):
        pass

    def help_page(self, have_set_interaction):
        if not have_set_interaction:
            set_interaction(self.soc, False)
        path = os.path.join(".", "docs", self.cmd + ".txt")
        if os.path.exists(path):
            with open(path) as f:
                send(self.soc, f.read(), newline=True)
        else:
            send(self.soc, "Docs to be implemented", newline=True)
