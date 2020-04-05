pipeline {
  agent {
    docker {
      image 'python:3.5'
      args '-u root'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ ; cd /tmp/build/'
        sh 'pip install --no-cache-dir -r src/requirements.txt'
        sh 'pip install ansible'
      }
    }
    stage('Test') {
      steps {
        sh 'cd /tmp/build/'
        sh 'cd src; python tests/test-app.py; cd ..'
        ansiblePlaybook(inventory: 'travis/inventory.list', playbook: 'ansible/setup.yml')
      }
    }
    stage('Deploy') {
      steps {
        sh '/usr/bin/true'
      }
    }
  }
}
