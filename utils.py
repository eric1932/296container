import os

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
            pass
        elif command[0] == "ps":
            print("UUID\t\tIMAGE\tCOMMAND\tCREATED\tSTATUS")
            for x in os.listdir("./container"):
                if os.path.isfile(os.path.join('container', x)):
                    print(x[:-4][:8])
        else:
            print("Command '" + command[0] + "' not found.")
            continue
