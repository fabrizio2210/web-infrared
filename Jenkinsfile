pipeline {
  agent any 
  environment {
    registryCredential = 'docker-login'
    buildDir = '/tmp/build'
    venvPackage = 'venv.tar'
    prefixPackage = 'web-infrared'
    installDir =  'opt/web-infrared'
    dockerCondition = '**CICD/Dockerfile.*'
    venvCondition = '**src/requirements.txt'
    debCondition = '**src/**'
    venvPackageStash = 'venv'
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
      when { 
        changeset venvCondition 
        beforeAgent true
      }
      steps {
        sh 'mkdir -p /${installDir} ; cp -rav * /${installDir} '
        sh 'cd /${installDir}; \
        python3 -m venv /${installDir}/venv/ ; \
        . /${installDir}/venv/bin/activate ; \
        pip3 install --no-cache-dir -r src/requirements.txt'
        sh 'tar -cvf ${venvPackage} -C /${installDir} venv/; chown 1000:996 ${venvPackage}'
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
      when { not { changeset venvCondition } }
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
          image 'fabrizio2210/web-infrared-controller' 
        }
      }
      when { 
        anyOf {
          changeset debCondition
          triggeredBy cause: "UserIdCause", detail: "fabrizio"
        }
        beforeAgent true
      }
      steps {
        unstash venvPackageStash
        sh 'mkdir -p ${buildDir} ; cp -rav * ${buildDir} '
        sh 'cd ${buildDir}; mkdir -p ${installDir}/'
				sh 'cd ${buildDir}; tar -xvf ${venvPackage} -C ${installDir}/'
				sh 'cd ${buildDir}; cp -rav src/* ${installDir}/'
        sh 'cd ${buildDir}; mkdir -p usr/share/doc/web-infrared/'
        sh 'cd ${buildDir}; cp DEBIAN/copyright usr/share/doc/web-infrared/'
        sh 'cd ${buildDir}; gzip -n9 DEBIAN/changelog'
        sh 'cd ${buildDir}; cp DEBIAN/changelog.gz usr/share/doc/web-infrared/'
        sh 'cd ${buildDir}; binarySize=$(du -cs usr/ opt/ | tail -1 | cut -f1); replaceString="s/__BINARY_SIZE__/"$binarySize"/"; sed -i $replaceString DEBIAN/control'
        sh 'cd ${buildDir}; versionStr=$(cat VERSION); sed -i "s/__VERSION__/"${versionStr}"/" DEBIAN/control'
        sh 'cd ${buildDir}; fakeroot tar czf data.tar.gz opt/ usr/'
        sh 'cd ${buildDir}; cd DEBIAN; fakeroot tar czf ../control.tar.gz control'
        sh 'cd ${buildDir}; echo 2.0 > debian-binary'
        sh 'cd ${buildDir}; versionStr=$(cat VERSION);fakeroot ar r ${prefixPackage}-$versionStr.deb debian-binary control.tar.gz data.tar.gz'
        sh 'mv ${buildDir}/${prefixPackage}-$(cat VERSION).deb .'
      }
      post {
        always {
          archiveArtifacts artifacts: prefixPackage + '-*.deb'
          archiveArtifacts artifacts: venvPackage
          cleanWs()
        }
      }
    }
  // Do test against the packet
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
          filter: prefixPackage + '-*.deb',
          selector: lastWithArtifacts()
        )
        echo "${currentBuild.buildCauses}" // same as currentBuild.getBuildCauses()
        sh 'dpkg -i ${prefixPackage}-*.deb'
        sh 'cd /${installDir}; . /${installDir}/venv/bin/activate ; python3 tests/test-app.py'
      }
    }
  // Do tests of Ansible playbook against an empty container
    stage('TestAnsible') {
      steps {
        script {
          docker.image('debian:stretch').withRun(){ c ->
            sh 'hostname'
            sh 'echo ${c.id}'
            sh 'echo $c'
            docker.image('fabrizio2210/web-infrared-controller').inside("--link ${c.id}:db"){
              sh 'echo ciao'
              //ansiblePlaybook(inventory: 'CICD/inventory.list', playbook: 'ansible/setup.yml')
            }
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


