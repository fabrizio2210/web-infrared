#!/bin/bash
set -x
set -e

cd $(dirname $0)

# Vagrant up
vagrant up

# Set infrastructure

ansible-playbook -i vagrant.py -i vagrant-groups.list ../setInfrared.yml

# Restart machine and rexport NFS sync folder if it is not present
if echo $(vagrant ssh -c "[ ! -d /opt/web-infrared/conf ] && echo REBOOT") | grep REBOOT ; then
  vagrant reload
fi
