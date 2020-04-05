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
        sh 'pip install --no-cache-dir -r src/requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'ls -la'
        sh 'python tests/test-app.py'
      }
    }
    stage('Deploy') {
      steps {
        sh '/usr/bin/true'
      }
    }
  }
}
