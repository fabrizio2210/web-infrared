#!/bin/bash
set -x
set -e

cd $(dirname $0)

# Vagrant up
vagrant up

# Set infrastructure

ansible-playbook -i vagrant.py -i vagrant-groups.list ../setApp.yml
vagrant ssh -c "cd /opt/web-infrared/ ; source venv/bin/activate; python tests/tests.py"
