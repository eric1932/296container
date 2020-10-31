# Container
## Author: Eric Liu, Longji Li
## Overview
We plan to implement a Linux container (LXC). The container allows one to make his or her app work across various platforms with high stability and get the app deployed without massive headaches, rewriting, and break-fixing. It has the necessary libraries, dependencies, and files so that one can move it through production without all of the nasty side effects. A container is essentially not a virtual machine. The former is at the level of the operating system, while the latter runs on host systems. Compared with traditional package managers, containers are more portable and can run on different operating systems (https://www.docker.com/resources/what-container).

## Purpose
Since LXC is a very broad idea, we do not have enough time to implement all features. The goal of our project includes some core features.
We would like to implement a container to establish easier packaging, multi-platform compatibility, and basic security via the sandbox mechanism.
We often need to deploy a bunch of services on different Linux servers. By using containers, we can speed up the process and save time on trivial configurations.

## Workload distribution
Zhaolong (Eric) would take care of doing research about packaging and deploying servers.  
Longji (Alex) would take care of doing research about isolation and building the file system.

## Features
Package programs and their dependencies; make deployment on different operating systems easier.  
A shell-like program/daemon that manages containers (eg. enable/disable, deploy/destroy).  
Network control, a client-server application.  

## Projected project milestones
### 1st month:  
Packaging/Deployment of containers  
  
### 2nd month:  
Container manager  
Sandbox -> Isolation (file)  
  
### 3rd month:  
Sandbox -> Network control  
Sandbox -> File System  
