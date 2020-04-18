import os
from time import time
from math import floor
import json
from uuid import UUID

CONFIG_PATH = './config'
PROPS = ['image', 'command', 'created_time']
if not os.path.exists(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)


def create_record(uuid: UUID, image: str, command: str):
    uuid = str(uuid)
    f = open(os.path.join(CONFIG_PATH, uuid + '.json'), 'w')
    d = {'image': image, 'command': command, 'created_time': floor(time())}
    json.dump(d, f)
    f.close()


def delete_record(uuid):
    if type(uuid) is not str:
        uuid = str(uuid)
    os.remove(os.path.join(CONFIG_PATH, uuid + '.json'))


def read_record(uuid) -> dict:
    if type(uuid) is not str:
        uuid = str(uuid)
    f = open(os.path.join(CONFIG_PATH, uuid + '.json'), 'r')
    data = json.load(f)
    data = {k: v for k, v in data.items() if k in PROPS}
    f.close()
    return data


def get_created_time(uuid: str):
    return read_record(uuid)['created_time']
