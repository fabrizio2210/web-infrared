#!/bin/bash
set -x
set -e

cd $(dirname $0)/test-vm/

# Vagrant up
vagrant up

# Set infrastructure
ansible-playbook -i ../vagrant.py -i ../vagrant-groups.list ../../setInfrared.yml

# Restart machine and rexport NFS sync folder if it is not present
if echo $(vagrant ssh -c "[ ! -d /opt/web-infrared/conf ] && echo REBOOT") | grep REBOOT ; then
  vagrant reload
fi

# Deploy App
ansible-playbook -i ../vagrant.py -i ../vagrant-groups.list ../../deployApp.yml

# Setup App
ansible-playbook -i ../vagrant.py -i ../vagrant-groups.list ../../setApp.yml

# Test
vagrant ssh -c "cd /opt/web-infrared/ ; source venv/bin/activate; python tests/test-infra.py"
