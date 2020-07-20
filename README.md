# A web remote control

![alt text](https://github.com/fabrizio2210/web-infrared/blob/master/images/web_remote_control.jpg "The hardware")

This web remote control is bornt to replace my broken remote control. Somebody can find as inspiration to implement his own.

# Goals

- Have got a working remote control
- No app installed on smartphone
- Adhere to CI/CD mechanism

# Installation

You need extra hardware:
- an IR shield
- optionally, an ethernet adapter

The installation is done by Ansible and Jenkins, but it can be done also manually. These commands are taken from Jenkinsfile:
```
 user@host:~ buildDir=/tmp/build
 user@host:~ installDir=opt/web-infrared
 user@host:~ venvPackage=venv.tar
 user@host:~ prefixPackage=web-infrared
 user@host:~ cd web-infrared/
 user@host:~/web-infrared mkdir -p ${buildDir} ; cp -rav * ${buildDir}
 user@host:~/web-infrared DEBIAN/venvCreation.sh -b ${buildDir} -i /${installDir} -o ${venvPackage}
 user@host:~/web-infrared mkdir -p ${buildDir} ; cp -rav * ${buildDir} 
 user@host:~/web-infrared DEBIAN/packetize.sh -b ${buildDir} -i ${installDir} -p ${venvPackage} -o . -f ${prefixPackage}
 user@host:~/web-infrared dpkg -i ./${prefixPackage}-*.deb

```
They should be executed on the target platform (i.e. raspberry) because are platworm dependent (e.g. armv6l).


## How CI/CD

- create test
..- use unit test for python
..- use infratest for Ansible part

- use tools to automate test and deploy
..- use Jenkins to do test and deploy

# Tests

The tests are in the folder tests. They will can be executed by script in a Vagrant environment, or individually executed by Jenkins or Travis.
