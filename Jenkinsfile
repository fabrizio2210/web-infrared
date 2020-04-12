pipeline {
  agent any 
  environment {
    registryCredential = 'docker-login'
  }
  stages {
  // Build a container that can be used among the pipeline
  // save it on Dockerhub
    stage('BuildDocker'){
      when { changeset "**CICD/Dockerfile.*" }
      steps {
        script {
          def controller = docker.build("fabrizio2210/web-infrared-controller:latest",  "-f CICD/Dockerfile.debian-stretch .")
          docker.withRegistry( '', registryCredential ) {
            controller.push()
          }
        }
      }
    }
  // Build the virtual env from requirements.txt
  // Save it for reuse
    stage('BuildVenv') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
          args '-u root'
        }
      }
      when { changeset "**src/requirements.txt" }
      steps {
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'cd /tmp/build/; \
        python3 -m venv /tmp/build/venv/ ; \
        . /tmp/build/venv/bin/activate ; \
        pip3 install --no-cache-dir -r src/requirements.txt'
        sh 'tar -cvf env.tar -C /tmp/build/ venv/; chown 1000:996 env.tar'
      }
      post {
        always {
          archiveArtifacts artifacts: 'env.tar'
        }
      }
    }
  // Create teh DEB package
  // Save it for the delivery
    stage('BuildDEB') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
        }
      }
      when { changeset "**src/**" }
      steps {
        copyArtifacts(
          projectName: env.JOB_NAME,
          selector: lastWithArtifacts()
        )
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'cd /tmp/build; mkdir -p opt/web-infrared/'
				sh 'cd /tmp/build; tar -xvf env.tar -C opt/web-infrared/'
				sh 'cd /tmp/build; cp -rav src/* opt/web-infrared/'
        sh 'cd /tmp/build; mkdir -p usr/share/locale/'
        sh 'cd /tmp/build; mkdir -p usr/share/doc/web-infrared/'
        sh 'cd /tmp/build; cp DEBIAN/copyright usr/share/doc/web-infrared/'
        sh 'cd /tmp/build; gzip -n9 DEBIAN/changelog'
        sh 'cd /tmp/build; cp DEBIAN/changelog.gz usr/share/doc/web-infrared/'
        sh 'cd /tmp/build; binarySize=$(du -cs usr/ opt/ | tail -1 | cut -f1); replaceString="s/__BINARY_SIZE__/"$binarySize"/"; sed -i $replaceString DEBIAN/control'
        sh 'cd /tmp/build; versionStr=$(cat VERSION); sed -i "s/__VERSION__/"${versionStr}"/" DEBIAN/control'
        sh 'cd /tmp/build; fakeroot tar czf data.tar.gz opt/ usr/'
        sh 'cd /tmp/build; cd DEBIAN; fakeroot tar czf ../control.tar.gz control'
        sh 'cd /tmp/build; echo 2.0 > debian-binary'
        sh 'cd /tmp/build; versionStr=$(cat VERSION);fakeroot ar r web-infrared-$versionStr.deb debian-binary control.tar.gz data.tar.gz'
        sh 'mv /tmp/build/web-infrared-$(cat VERSION).deb .'
      }
      post {
        always {
          archiveArtifacts artifacts: 'web-infrared-*.deb'
        }
      }
    }
  // Do test against the Code
    stage('TestCode') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
          args '-u root'
        }
      }
      steps {
        copyArtifacts(
          projectName: env.JOB_NAME,
          selector: lastWithArtifacts()
        )
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'tar -xvf env.tar -C /tmp/build/'
        sh 'cd /tmp/build/; . /tmp/build/venv/bin/activate ; cd src; python3 tests/test-app.py'
      }
    }
  // Do tests of Ansible playbook against an empty container
    stage('TestAnsible') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
          args '-u root'
        }
      }
      steps {
        ansiblePlaybook(inventory: 'CICD/inventory.list', playbook: 'ansible/setup.yml')
        //TODO: insert infra test
      }
    }
  // Deploy the configuration with Ansible
    stage('DeployConfiguration') {
      steps {
        sh 'pwd'
      }
    }
  // Deploy the DEB package
    stage('DeployDEB') {
      steps {
        sh 'pwd'
      }
    }
  }
}


