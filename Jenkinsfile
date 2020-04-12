pipeline {
  agent any 
  environment {
    registryCredential = 'docker-login'
  }
  stages {
    stage('BuildDocker'){
      when { changeset "**CICD/**" }
      steps {
        script {
          def controller = docker.build("fabrizio2210/web-infrared-controller:latest",  "-f CICD/Dockerfile.debian-stretch .")
          docker.withRegistry( '', registryCredential ) {
            controller.push()
          }
        }
      }
    }
    stage('Build') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
          args '-u root'
        }
      }
      when { changeset "**src/**" }
      steps {
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'cd /tmp/build/; \
        python3 -m venv /tmp/build/venv/ ; \
        . /tmp/build/venv/bin/activate ; \
        pip3 install --no-cache-dir -r src/requirements.txt'
        sh 'tar -cvf env.tar -C /tmp/build/ venv/; chown 1000:996 build.tar'
      }
      post {
        archiveArtifacts artifacts: 'env.tar'
      }
    }
    stage('Test') {
      agent {
        docker { 
          image 'fabrizio2210/web-infrared-controller' 
          args '-u root'
        }
      }
      steps {
        copyArtifacts(
          projectName: env.JOB_NAME
        )
        script {
          currentBuild.upstreamBuilds?.each { b ->
            echo b.getFullProjectName()
          }
        }
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'tar -xvf env.tar -C /tmp/build/'
        sh 'cd /tmp/build/; . /tmp/build/venv/bin/activate ; cd src; python3 tests/test-app.py'
        ansiblePlaybook(inventory: 'travis/inventory.list', playbook: 'ansible/setup.yml')
      }
    }
    stage('Deploy') {
      steps {
        sh 'pwd'
      }
    }
  }
}


