import os
import subprocess
from uuid import uuid1

from cgroups import Cgroup
from sh import mount, cp, umount


def run(uuid: str = None, load: bool = False) -> None:
    cgroup_name = 'test'
    base_image = './base_images/ubuntu.img'
    if not uuid:
        uuid = uuid1()
    container_name = str(uuid) + '.img'
    img_path = os.path.join('container', container_name)
    mount_path = './container/' + str(uuid)

    if not load:
        cp(base_image, img_path)
    if not os.path.exists(mount_path):
        os.mkdir(mount_path)
    mount('-o', 'rw', img_path, mount_path)

    cg = Cgroup(cgroup_name)
    cg.set_cpu_limit(50)
    cg.set_memory_limit(512)

    print("uuid:", uuid)

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
    proc = subprocess.Popen('/bin/bash', preexec_fn=hook, cwd=mount_path, env=my_env)
    proc.wait()

    # cleanup
    umount(mount_path)
    os.rmdir(mount_path)
