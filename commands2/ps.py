import getopt
import socket
from datetime import datetime

import config
from Command import Command
from utils import get_all_containers
from utils import get_running_containers
from utils import send
from utils import set_interaction


class Ps(Command):
    def __init__(self, soc: socket.socket, args: list):
        super().__init__(soc, "ps", args)

    def handle(self):
        set_interaction(self.soc, False)
        optlist, args = getopt.getopt(self.args, 'ah', ['help', 'all'])
        if ('-h', '') in optlist or ('--help', '') in optlist:
            self.help_page(True)
        else:
            flag_show_all = True if ('-a', '') in optlist or ('--all', '') in optlist else False
            running = get_running_containers()
            send(self.soc, "UUID\t\tIMAGE\tCOMMAND\t\tCREATED\t\t\tSTATUS", newline=True)
            for uuid in (get_all_containers() if flag_show_all else running):
                data = config.read_record(uuid)
                compose = uuid[:8] + "\t" + \
                          data['image'] + "\t" + \
                          (data['command'] if type(data['command']) is str else (" ".join(data['command']))[
                                                                                :50]) + "\t" + \
                          datetime.fromtimestamp(data['created_time']).strftime("%Y-%m-%d %H:%M:%S") + "\t" + \
                          ("Up" if (not flag_show_all) or (uuid in running) else "Exited")
                # TODO command length limit
                send(self.soc, compose, newline=True)
            # if flag_show_all:
            #     all_containers = get_all_containers()
            #     for uuid in all_containers:
            #         data = config.read_record(uuid)
            #         compose = uuid[:8] + "\t" + \
            #                   data['image'] + "\t" + \
            #                   (data['command'] if type(data['command']) is str else (" ".join(data['command']))[:50]) + "\t" + \
            #                   datetime.fromtimestamp(data['created_time']).strftime("%Y-%m-%d %H:%M:%S") + "\t" + \
            #                   ("Up" if uuid in running else "Exited")
            #         # TODO command length limit
            #         send(self.soc, compose, newline=True)
            # else:
            #     for uuid in running:
            #         data = config.read_record(uuid)
            #         compose = uuid[:8] + "\t" + \
            #                   data['image'] + "\t" + \
            #                   (data['command'] if type(data['command']) is str else (" ".join(data['command']))[:50]) + "\t" + \
            #                   datetime.fromtimestamp(data['created_time']).strftime("%Y-%m-%d %H:%M:%S") + "\t" + \
            #                   "Up"
            #         # TODO command length limit
            #         send(self.soc, compose, newline=True)
