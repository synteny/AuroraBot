#!/bin/bash

fallocate -l 1G /swapfile
chmod 600 /swapfile 
mkswap /swapfile
swapon /swapfile
cat "/swapfile   none    swap    sw    0   0" >> /etc/fstab
sysctl vm.swappiness=10
sysctl vm.vfs_cache_pressure=50
cat "vm.swappiness = 10" >> /etc/sysctl.conf
cat "vm.vfs_cache_pressure = 50" >> /etc/sysctl.conf
