pipeline {
  agent any 
  stages {
    stage('BuildDocker'){
      when { changeset "**CICD/**" }
      steps {
        script {
          def controller = docker.build("fabrizio2210/web-infrared-controller:latest",  "CICD/Dockerfile.debian-stretch")
          controller.push()
        }
      }
    }
    stage('Build') {
      when { changeset "**src/**" }
      steps {
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ '
        sh 'cd /tmp/build/; \
        python3 -m venv ; \
        pip3 install --no-cache-dir -r src/requirements.txt'
        archiveArtifacts artifacts: '/tmp/build/venv/'
      }
    }
    stage('Test') {
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

