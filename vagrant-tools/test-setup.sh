#!/bin/bash
set -x
set -e

cd $(dirname $0)/test-vm/

# Vagrant up
vagrant up

# Setup all
ansible-playbook -i ../vagrant.py -i ../vagrant-groups.list ../../ansible/setup.yml

# Test
vagrant ssh -c "cd /opt/web-infrared/ ; source venv/bin/activate; python tests/test-infra.py"
