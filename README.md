# 296 Container
### Author: Eric Liu, Longji Li

## Usage
1. Use `vagrant up` to set up the environment.

Then, run
```shell
vagrant ssh
sudo -i
cd /296container
python3 ./server.py
```
To start the server.

In another terminal, do the first 3 lines as well.
```shell
python3 ./client.py
```

### Examples
- Ubuntu bash
  ```shell
  python3 ./client.py run ubuntu /bin/bash
  ```
- Nginx server
  ```shell
  python3 ./client.py run nginx /usr/sbin/nginx -g "\"daemon off;\""
  ```

## Overview
We plan to implement a Linux container (LXC). The container allows one to make his or her app work across various platforms with high stability and get the app deployed without massive headaches, rewriting, and break-fixing. It has the necessary libraries, dependencies, and files so that one can move it through production without all of the nasty side effects. A container is essentially not a virtual machine. The former is at the level of the operating system, while the latter runs on host systems. Compared with traditional package managers, containers are more portable and can run on different operating systems (https://www.docker.com/resources/what-container).

## Purpose
Since LXC is a very broad idea, we do not have enough time to implement all features. The goal of our project includes some core features.
We would like to implement a container to establish easier packaging, multi-platform compatibility, and basic security via the sandbox mechanism.
We often need to deploy a bunch of services on different Linux servers. By using containers, we can speed up the process and save time on trivial configurations.

## Workload distribution
Eric would take care of doing research about packaging and deploying servers.  
Longji would take care of doing research about isolation and building the file system.

## Features
Package programs and their dependencies; make deployment on different operating systems easier.  
A shell-like program/daemon that manages containers (eg. enable/disable, deploy/destroy).  
Network control, a client-server application.  

[comment]: <> (## Projected project milestones)

[comment]: <> (### 1st month:  )

[comment]: <> (Packaging/Deployment of containers  )
  
[comment]: <> (### 2nd month:  )

[comment]: <> (Container manager  )

[comment]: <> (Sandbox -> Isolation &#40;file&#41;  )
  
[comment]: <> (### 3rd month:  )

[comment]: <> (Sandbox -> Network control  )

[comment]: <> (Sandbox -> File System  )
