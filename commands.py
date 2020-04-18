import getopt
import os
import socket
from datetime import datetime

import config
from utils import send, send_arg, find_uuid, set_interaction, get_running_containers, get_all_containers


def main_help(soc: socket.socket):
    set_interaction(soc, False)
    send(soc, "commands: help exit run ps", newline=True)


def ps(soc: socket.socket, args: list):
    set_interaction(soc, False)
    optlist, args = getopt.getopt(args, 'ah', ['help', 'all'])
    if ('-h', '') in optlist or ('--help', '') in optlist:
        # TODO print help
        pass
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
    if len(optlist) == 0 and len(args) == 0 or ('--help', '') in optlist:
        set_interaction(soc, False)
        # print usage
        send(soc, "\"run\" requires at least 1 argument.\n"
                  "See \"run --help\"\n"
                  "\n"
                  "Usage: run [UUID] IMAGE\n"
                  "\n"
                  "Run a command in a container. If UUID is specified, do not create a new one.\n")
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
    # TODO help page
    uuid_to_remove = find_uuid(args[0])
    if not uuid_to_remove:
        send(soc, "Cannot find container: " + args[0], newline=True)
    elif uuid_to_remove in get_running_containers():
        send(soc, "Cannot remove a running container!", newline=True)
    else:
        os.remove(os.path.join("container", uuid_to_remove + '.img'))
        config.delete_record(uuid_to_remove)
        send(soc, uuid_to_remove + " is removed", newline=True)
