pipeline {
  agent any
  stages {
    stage('Build') {
      agent {
        docker {
          image 'python:3.5'
        }

      }
      steps {
        sh 'pip install -r src/requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh '/usr/bin/true'
      }
    }
    stage('Deploy') {
      steps {
        sh '/usr/bin/true'
      }
    }
  }
}