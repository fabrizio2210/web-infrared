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
        source /tmp/build/venv/bin/activate ; \
        pip3 install --no-cache-dir -r src/requirements.txt'
        archiveArtifacts artifacts: '/tmp/build/venv/'
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
        sh 'cd /tmp/build/; cd src; python3 tests/test-app.py; cd ..'
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

