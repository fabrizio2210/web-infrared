pipeline {
  agent any 
  environment {
    registryCredential = 'docker-login'
    buildDir = '/tmp/build'
    venvPackage = 'venv.tar'
    prefixPackage = 'web-infrared'
    installDir =  'opt/web-infrared'
    dockerCondition = '**CICD/Dockerfile*'
    venvCondition = '**src/requirements.txt'
    debCondition = '**src/**'
    debCondition2 = '**DEBIAN/**'
    debPackageStash = 'deb'
    venvPackageStash = 'venv'
    controllerImage = 'web-infrared-controller'
    targetImage = 'web-infrared-target'
  }
  stages {
  // Build a container that can be used among the pipeline
  // save it on Dockerhub
    stage('BuildDocker'){
      when { 
        changeset dockerCondition
        beforeAgent true
      }
      steps {
        script {
          def controller = docker.build('fabrizio2210/' + controllerImage + ':latest',  '-f CICD/Dockerfile-' + controllerImage + '.debian-stretch .')
          def target = docker.build('fabrizio2210/' + targetImage + ':latest',  '-f CICD/Dockerfile-' + targetImage + '.debian-stretch .')
          docker.withRegistry( '', registryCredential ) {
            controller.push()
            target.push()
          }
        }
      }
    }
  // Build the virtual env from requirements.txt
  // Save it for reuse
    stage('BuildVenv') {
      agent {
        docker { 
          image 'fabrizio2210/' + controllerImage 
          args '-u root'
        }
      }
      when { 
        changeset venvCondition 
        beforeAgent true
      }
      steps {
        sh 'mkdir -p ${buildDir} ; cp -rav * ${buildDir} '
        sh 'DEBIAN/venvCreation.sh -b ${buildDir} \
                                   -i /${installDir} \
                                   -o ${venvPackage}'
        sh 'chown 1000:996 ${venvPackage}'
      }
      post {
        always {
          stash includes: venvPackage, name: venvPackageStash
          archiveArtifacts artifacts: venvPackage
          cleanWs()
        }
      }
    }
  // Collect venv from old archives
    stage ('collectVenv'){
      when { 
        not { changeset venvCondition } 
        beforeAgent true
      }
      steps {
        copyArtifacts(
          projectName: env.JOB_NAME,
          filter: venvPackage,
          selector: lastWithArtifacts()
        )
        stash includes: venvPackage, name: venvPackageStash
      }
    }
  // Create teh DEB package
  // Save it for the delivery
    stage('BuildDEB') {
      agent {
        docker { 
          image 'fabrizio2210/' + controllerImage 
        }
      }
      when { 
        anyOf {
          changeset debCondition
          changeset debCondition2
          triggeredBy cause: "UserIdCause", detail: "fabrizio"
        }
        beforeAgent true
      }
      steps {
        unstash venvPackageStash
        sh 'mkdir -p ${buildDir} ; cp -rav * ${buildDir} '
        sh 'DEBIAN/packetize.sh -b ${buildDir} \
                                -i ${installDir} \
                                -p ${venvPackage} \
                                -o . \
                                -f ${prefixPackage}'
      }
      post {
        always {
          stash includes: prefixPackage + '-*.deb', name: debPackageStash
          archiveArtifacts artifacts: prefixPackage + '-*.deb'
          archiveArtifacts artifacts: venvPackage
          cleanWs()
        }
      }
    }
  // Collect Deb from old archives
    stage ('collectDeb'){
      when { 
        not { 
          anyOf {
            changeset debCondition
            changeset debCondition2
          }
        }
        beforeAgent true
      }
      steps {
        copyArtifacts(
          projectName: env.JOB_NAME,
          filter: prefixPackage + '-*.deb',
          selector: lastWithArtifacts()
        )
        stash includes: prefixPackage + '-*.deb', name: debPackageStash
      }
    }
  // Do test against the packet
    stage('TestCode') {
      agent {
        docker { 
          image 'fabrizio2210/' + controllerImage 
          args '-u root'
        }
      }
      steps {
        unstash debPackageStash
        echo "${currentBuild.buildCauses}" // Display who is triggering
        sh 'dpkg -i ./${prefixPackage}-*.deb'
        sh 'cd /${installDir}; . /${installDir}/venv/bin/activate ; python3 tests/test-app.py'
      }
    }
  // Do tests of Ansible playbook against an empty container
    stage('TestAnsible') {
      agent {
        docker { 
          image 'fabrizio2210/' + controllerImage 
          args '-u root -e PATH=$PATH:/var/jenkins_home/bin'
        }
      }
      steps {
        unstash debPackageStash
        script {
          docker.image('fabrizio2210/' + targetImage).withRun('','tail -f /dev/null'){ c ->
            sh 'hostname'
            echo "${c.id}"
            sh 'sed -i -e "s/target/' + "${c.id}" + '/" CICD/inventory.list'
            ansiblePlaybook(inventory: 'CICD/inventory.list', playbook: 'ansible/setup.yml', extras: '-e src_dir=' + env.WORKSPACE )
          }
        }
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


