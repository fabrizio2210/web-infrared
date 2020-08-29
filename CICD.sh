#!/bin/bash

set -e
set -u
set -x
#############
# Environment

registryCredential='docker-login'
buildDir='/tmp/build'
venvPackage='venv.tar'
prefixPackage='web-infrared'
installDir='opt/web-infrared'
dockerCondition='CICD/Dockerfile'
venvCondition='src/requirements.txt'
debCondition='src/\|DEBIAN/'
debPackageStash='deb'
venvPackageStash='venv'
controllerImage='web-infrared-controller'
targetImage='web-infrared-target'

runRepository="$(mktemp -d)"
workspace=$(dirname $0)
if ! echo $workspace |  grep "^/" ;  then
  workspace="$(pwd)/$workspace"
fi
repository='/tmp'
changedFiles="$(git diff --name-only HEAD^1 HEAD)"

#  post {
#    success {
#      telegramSend(message: 'Web infrared build succesfully', chatId: 10584874)
#    }
#    failure {
#      telegramSend(message: 'Error: Web infrared build has a build problem', chatId: 10584874)
#    }
#  }

#############
# BuildDocker
## Build a container that can be used among the pipeline
## save it on Dockerhub

#TODO push  images on DockerHUB
if echo "$changedFiles" | grep -q $dockerCondition ; then
  docker build -t fabrizio2210/${controllerImage}:latest -f CICD/Dockerfile-${controllerImage}.debian-stretch .
  docker build -t fabrizio2210/${targetImage}:latest -f CICD/Dockerfile-${targetImage}.debian-stretch .
  #docker.withRegistry( '', registryCredential ) {
  #  controller.push()
  #  target.push()
  #}
fi

###########
# BuildVenv
## Build the virtual env from requirements.txt
## Save it for reuse

#TODO build on armv6l architecture (infrarosso.oss)
if [ ! -e ${repository}/${venvPackage} ] || echo "$changedFiles" | grep -q $venvCondition ; then
container=$(docker run -d fabrizio2210/${controllerImage} tail -f /dev/null)
docker exec ${container} mkdir -p ${buildDir}
docker cp . ${container}:${buildDir}
docker exec ${container} ls  -l /tmp/build
docker exec ${container} ${buildDir}/DEBIAN/venvCreation.sh -b ${buildDir} -i /${installDir} -o ${venvPackage}
docker cp ${container}:${venvPackage} .
docker container rm --force ${container}
  cp ${venvPackage} ${repository}/
  rm ${venvPackage}
fi

##########
# BuildDEB
## Create the DEB package
## Save it for the delivery

if [ ! -e ${repository}/${prefixPackage}-$(cat VERSION).deb ] || echo $changedFiles | grep "$debCondition" ; then
  container=$(docker run -d fabrizio2210/${controllerImage} tail -f /dev/null)
  docker exec ${container} mkdir -p ${buildDir}
  cp ${repository}/${venvPackage} $workspace/
  rm ${prefixPackage}*.deb || /bin/true
  docker cp . ${container}:${buildDir}
  docker exec ${container} ${buildDir}/DEBIAN/packetize.sh -b ${buildDir} \
                                                         -i ${installDir} \
                                                        -p ${venvPackage} \
                                                                     -o . \
                                                        -f ${prefixPackage}
  rm $workspace/${venvPackage}
  docker exec ${container} ls  -l 
  docker cp ${container}:/${prefixPackage}-$(cat VERSION).deb ${repository}/
  docker container rm --force ${container}
fi

##########
# TestCode

container=$(docker run -d fabrizio2210/${controllerImage} tail -f /dev/null)
docker cp . ${container}:${buildDir}
docker cp ${repository}/${prefixPackage}-$(cat VERSION).deb ${container}:/   
docker exec ${container} bash -c "ln -s /bin/true /usr/bin/irsend"
docker exec ${container} bash -c "dpkg -i ./${prefixPackage}-*.deb"
docker exec ${container} bash -c "cd /${installDir}; . /${installDir}/venv/bin/activate ; python3 tests/test-app.py"
docker container rm --force ${container}


#############
# TestAnsible

docker network inspect Jenkins_default || docker network create --attachable Jenkins_default
docker container rm target --force || /bin/true
container=$(docker run -d --network=Jenkins_default fabrizio2210/${controllerImage} tail -f /dev/null)
docker exec ${container} mkdir -p ${buildDir}
docker cp . ${container}:${buildDir}
docker cp ${repository}/${prefixPackage}-$(cat VERSION).deb ${container}:${buildDir}/   
#docker service create --name=target --network=Jenkins_default --mount type=bind,source=/sys/fs/cgroup,destination=/sys/fs/cgroup,ro=1 --constraint node.hostname!=raspberrypi0 fabrizio2210/${targetImage}
docker run -d --name=target --network=Jenkins_default --privileged=true --mount type=bind,source=/sys/fs/cgroup,destination=/sys/fs/cgroup,ro=1 fabrizio2210/${targetImage}
docker exec ${container} bash -c "cd ${buildDir}; ansible-playbook -i CICD/inventory.list ansible/setup.yml -e src_folder=${buildDir}"
docker container rm --force ${container}
docker container rm target --force

exit 0
  // Deploy the configuration and DEB with Ansible
    stage('DeployConfiguration') {
      agent {
        docker { 
          image 'fabrizio2210/' + controllerImage 
          args '-u root -e PATH=$PATH:/var/jenkins_home/bin'
        }
      }
      steps {
        sh 'rm ${prefixPackage}*.deb || /bin/true '
        unstash debPackageStash
        ansiblePlaybook(credentialsId: 'id_oss_deploy', inventory: 'ansible/hosts.list', playbook: 'ansible/setup.yml', extras: '-e src_folder=' + env.WORKSPACE )
      }
    }
  }
}
