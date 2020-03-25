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
    while True:
        command = input("$ ")
        command = command.split()
        if command[0] == "exit":
            break
        elif command[0] == "help":
            print("commands: help exit run ls")
        elif command[0] == "run":
            if len(command) == 1:
                run()
            elif len(command) == 2:
                uuid = find_uuid(command[1])
                if uuid:
                    run(uuid)
                else:
                    print("No matching uuid found!")
            elif len(command) == 3:
                uuid = find_uuid(command[1])
                if not uuid:
                    print("No matching uuid found!")
                elif command[2] == "--continue":
                    run(uuid, True)
                else:
                    run(uuid, False)
        elif command[0] == "demo":
            run('8e07cd5e-635d-11ea-9fe3-2df319929fc7', False)
        elif command[0] == "ls":
            for x in os.listdir("./container"):
                print(x[:-4])
        else:
            continue