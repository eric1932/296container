import os
import socket


def find_uuid(short):
    uuids = [x[:-4] for x in os.listdir("./container") if x.endswith(".img")]
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


# TODO remove
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


def send(soc: socket.socket, msg, newline=False):
    soc.send((str(msg) + ("\n" if newline else "")).encode())


def send_arg(soc: socket.socket, key, value):
    soc.send(("%04d" % (len(key) + 1 + len(value)) +
              key + "=" + value).encode())


def set_interaction(soc: socket.socket, flag: bool):
    soc.send(str(int(flag)).encode())


def get_running_containers():
    return [uuid for uuid in os.listdir("./container") if os.path.isdir(os.path.join("./container", uuid))]


def get_all_containers():
    return [uuid_img[:-4] for uuid_img in os.listdir("./container") if uuid_img[-4:] == ".img"]

def get_entry_point(image: str):
    assert os.path.exists(os.path.join("base_images", image + ".img"))
    txt_path = os.path.join("base_images", image + ".txt")
    assert os.path.exists(txt_path)
    with open(txt_path) as f:
        str = f.read()
    assert str[-1] != '\n'
    return str
