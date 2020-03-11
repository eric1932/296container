import os
import subprocess
from uuid import uuid1

from cgroups import Cgroup
from sh import mount, cp, umount


def run():
    if not os.path.exists('./container'):
        os.mkdir('./container')
    cgroup_name = 'test'
    base_image = './base_images/ubuntu.img'
    uuid = uuid1()
    container_name = str(uuid) + '.img'
    img_path = './container/' + container_name
    mount_path = './container/' + str(uuid)

    cp(base_image, img_path)
    os.mkdir(mount_path)
    mount('-o', 'rw', img_path, mount_path)

    cg = Cgroup(cgroup_name)
    cg.set_cpu_limit(50)
    cg.set_memory_limit(512)

    def hook():
        cg.add(os.getpid())
        os.chroot('.')
    # proc = subprocess.Popen('echo hello world subprocess!', shell=True)
    # proc = subprocess.Popen(['ls', '-lah'], shell=False)
    # proc = subprocess.Popen(['free', '-h'], preexec_fn=hook, shell=False)
    proc = subprocess.Popen('/bin/bash', preexec_fn=hook, cwd=mount_path)
    proc.wait()

    # cleanup
    umount(mount_path)
    os.rmdir(mount_path)


if __name__ == '__main__':
    run()
