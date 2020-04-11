pipeline {
  agent {
    docker {
      image 'debian:stretch'
      args '-u root'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'mkdir -p /tmp/build/ ; cp -rav * /tmp/build/ ; cd /tmp/build/'
        sh 'apt-get update -y && apt-get install -y --no-install-recommends \
            software-properties-common \
            build-essential \
            libffi-dev \
            libssl-dev \
            python3-dev \
            python3-pip \
            sudo \
            git \
            systemd \
            && rm -rf /var/lib/apt/lists/*'
        sh 'pip3 install --upgrade setuptools && pip3 install ansible'
        sh 'pip3 install --no-cache-dir -r src/requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'cd /tmp/build/; cd src; python tests/test-app.py; cd ..'
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
