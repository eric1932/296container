import os
import shutil
import subprocess
import sys
from uuid import uuid1

from cgroups import Cgroup
from sh import mount, umount

from config import create_record

# TODO tmp
processes = {}  # define {uuid: (Popen, mount_path)}


def run(detach: bool, image: str = 'ubuntu.img', uuid: str = None, load: bool = False, cmd=('/bin/uname', '-a')) -> None:
    cgroup_name = 'test'
    base_image_path = os.path.join('./base_images/', image)  # TODO exist?
    if not uuid:
        uuid = uuid1()
    container_name = str(uuid) + '.img'
    img_path = os.path.join('container', container_name)
    mount_path = './container/' + str(uuid)

    if not load:
        shutil.copy(base_image_path, img_path)
    if not os.path.exists(mount_path):
        os.mkdir(mount_path)
    mount('-o', 'rw', img_path, mount_path)

    cg = Cgroup(cgroup_name)
    cg.set_cpu_limit(50)
    cg.set_memory_limit(512)

    print("uuid:", uuid)  # TODO remove

    # create record
    create_record(uuid, "ubuntu", cmd)  # TODO replace ubuntu

    # env
    my_env = os.environ.copy()
    path = set(my_env["PATH"].split(":"))
    path.add("/bin")
    path.add("/sbin")
    path.add("/usr/bin")
    path.add("/usr/sbin")
    path.add("/usr/local/bin")
    path.add("/usr/local/sbin")
    my_env["PATH"] = ":".join(path)

    def hook():
        cg.add(os.getpid())
        os.chroot('.')

    # proc = subprocess.Popen('echo hello world subprocess!', shell=True)
    # proc = subprocess.Popen(['ls', '-lah'], shell=False)
    # proc = subprocess.Popen(['free', '-h'], preexec_fn=hook, shell=False)
    proc = subprocess.Popen(cmd, preexec_fn=hook, cwd=mount_path, env=my_env)
    # TODO try catch

    # stdout_r, stdout_w = os.pipe()
    # stdout_r = os.fdopen(stdout_r)
    # stdout_w = os.fdopen(stdout_w, 'w')
    # proc = subprocess.Popen('/bin/bash', preexec_fn=hook, cwd=mount_path, env=my_env,
    #                         stdin=subprocess.PIPE, stdout=stdout_w, stderr=subprocess.STDOUT,
    #                         universal_newlines=True)
    # # proc.stdin.write(b'ls /\n')
    # # proc.stdin.flush()
    # # while True:
    # #     buf = stdout_r.readline()
    # #     if not buf:
    # #         break
    # # redirect_socket.send(buf)
    # # buf = redirect_socket.recv(1024)
    # # proc.stdin.write(buf)
    # print("Input: ", end="", file=stdout_w, flush=True)
    # print(redirect_socket.recv(1024).decode(), file=proc.stdin, flush=True)
    # buf = stdout_r.readline()
    # redirect_socket.send(buf.encode())

    if detach:
        # TODO add to pool
        processes[str(uuid)] = (proc, mount_path)
    else:
        proc.wait()
        # cleanup
        umount(mount_path)
        os.rmdir(mount_path)


def terminate(uuid: str):
    if uuid not in processes:
        print("unexpected behavior", file=sys.stderr)
        # TODO
    else:
        proc, mount_path = processes[uuid]
        proc.terminate()
        proc.wait()
        # cleanup
        umount(mount_path)
        os.rmdir(mount_path)
