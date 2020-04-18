import getopt
import os
import socket
from datetime import datetime

import config
from utils import send, send_arg, find_uuid, set_interaction, get_running_containers, get_all_containers


def main_help(soc: socket.socket):
    set_interaction(soc, False)
    with open("docs/help.txt") as f:
        send(soc, f.read(), newline=True)


def ps(soc: socket.socket, args: list):
    set_interaction(soc, False)
    optlist, args = getopt.getopt(args, 'ah', ['help', 'all'])
    if ('-h', '') in optlist or ('--help', '') in optlist:
        with open("docs/ps.txt") as f:
            send(soc, f.read(), newline=True)
    else:
        flag_show_all = True if ('-a', '') in optlist or ('--all', '') in optlist else False
        running = get_running_containers()
        send(soc, "UUID\t\tIMAGE\tCOMMAND\t\tCREATED\t\t\tSTATUS", newline=True)
        if flag_show_all:
            all_containers = get_all_containers()
            for uuid in all_containers:
                data = config.read_record(uuid)
                compose = uuid[:8] + "\t" +\
                          data['image'] + "\t" +\
                          data['command'] + "\t" +\
                          datetime.fromtimestamp(data['created_time']).strftime("%Y-%m-%d %H:%M:%S") + "\t" +\
                          ("Up" if uuid in running else "Exited")
                # TODO command length limit
                send(soc, compose, newline=True)
        else:
            for uuid in running:
                data = config.read_record(uuid)
                compose = uuid[:8] + "\t" + \
                          data['image'] + "\t" + \
                          data['command'] + "\t" + \
                          datetime.fromtimestamp(data['created_time']).strftime("%Y-%m-%d %H:%M:%S") + "\t" + \
                          "Up"
                # TODO command length limit
                send(soc, compose, newline=True)


def run(soc: socket.socket, args: list):
    optlist, args = getopt.getopt(args, 'h', ['help'])
    if len(optlist) == 0 and len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
        set_interaction(soc, False)
        with open("docs/run.txt") as f:
            send(soc, f.read(), newline=True)
    elif len(args) == 1:
        set_interaction(soc, True)
        send(soc, "next")  # end of passing args
    elif len(args) == 2:
        uuid = find_uuid(args[0])
        if uuid:
            set_interaction(soc, True)
            send_arg(soc, "uuid", uuid)
            send_arg(soc, "load", "1")
            send(soc, "next")  # end of passing args
        else:
            set_interaction(soc, False)
            send(soc, "No matching uuid found!", newline=True)
    else:
        pass


def start(soc: socket.socket, args: list):
    pass


def rm(soc: socket.socket, args: list):
    optlist, args = getopt.getopt(args, 'h', ['help'])
    set_interaction(soc, False)
    if len(optlist) == 0 and len(args) == 0 or ('--help', '') in optlist or ('-h', '') in optlist:
        with open("docs/rm.txt") as f:
            send(soc, f.read(), newline=True)
    else:
        uuid_to_remove = find_uuid(args[0])
        if not uuid_to_remove:
            send(soc, "Cannot find container: " + args[0], newline=True)
        elif uuid_to_remove in get_running_containers():
            send(soc, "Cannot remove a running container!", newline=True)
        else:
            os.remove(os.path.join("container", uuid_to_remove + '.img'))
            config.delete_record(uuid_to_remove)
            send(soc, uuid_to_remove + " is removed", newline=True)
