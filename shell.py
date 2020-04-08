#!/usr/bin/env python3

import os
import readline

from run import run


def find_uuid(short):
    uuids = [x[:-4] for x in os.listdir("./container")]
    found = False
    target = None
    for x in uuids:
        if x.startswith(short):
            if found:
                found = False
                break
            else:
                target = x
                found = True
    if found:
        return target
    else:
        return None


def parser_run(args):
    if len(args) == 1:
        # print usage
        print("\"run\" requires at least 1 argument.")
        print("See \"run --help\"")
        print()
        print("Usage: run [UUID] IMAGE")
        print()
        print("Run a command in a container. If UUID is specified, do not create a new one.")
    elif len(args) == 2:
        run()
    elif len(args) == 3:
        uuid = find_uuid(args[1])
        if uuid:
            run(uuid, True)
        else:
            print("No matching uuid found!")


if __name__ == '__main__':
    # initialize folders
    if not os.path.exists('./container'):
        os.mkdir('./container')

    while True:
        command = input("$ ")
        command = command.split()
        if not len(command):
            continue
        elif command[0] == "exit":
            print("See you.")
            break
        elif command[0] == "help":
            print("commands: help exit run ps")
        elif command[0] == "run":
            parser_run(command)
        elif command[0] == "ps":
            print("UUID\t\tIMAGE\tCOMMAND\tCREATED\tSTATUS")
            for x in os.listdir("./container"):
                if os.path.isfile(os.path.join('container', x)):
                    print(x[:-4][:8])
        else:
            print("Command '" + command[0] + "' not found.")
            continue
