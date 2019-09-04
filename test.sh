#!/bin/bash
set -x
set -e

_pwd=$PWD
tempDir=$(mktemp -d)

# Vagrant up
vagrant up

# Set infrastructure

ansible-playbook -i vagrant.py -i vagrant-groups.list setWebserver-infrared.yml



[ -n "$tempDir" ] && rm -rf "$tempDir"
