// Reference: https://gist.github.com/JCotton1123/a9746529b88c4a07e422cb4b59cbe329
pipeline {
  options {
    buildDiscarder(logRotator(numToKeepStr: '10')) // Retain history on the last 10 builds
    ansiColor('xterm') // Enable colors in terminal
    timestamps() // Append timestamps to each line
    timeout(time: 20, unit: 'MINUTES') // Set a timeout on the total execution time of the job
  }
  agent any
  stages {  // Define the individual processes, or stages, of your CI pipeline
    stage('Checkout') { // Checkout (git clone ...) the projects repository
      steps {
        checkout scm
      }
    }
    stage('Setup') { // Install any dependencies you need to perform testing
      steps {
        script {
          sh """
          python3 -m pip install pytest && pytest --version 
          """
        }
      }
    }
    stage('Linting') { // Run pylint against your code
      steps {
        script {
          sh """
          pylint **/*.py
          """
        }
      }
    }
    stage('Verify tooling'){ // https://www.youtube.com/watch?v=ZPD_PzGOvFM&t=168s (How to use docker compose with Jenkins)
      steps{
        sh '''
        docker version
        docker compose version
        curl --version 
        '''
      }
    }
    stage('Build the docker image cat_data_watcher:latest'){//Use the bash script build.sh (Ran sudo chmod +x build.sh to make it executable here)
      steps{ 
        sh './build.sh'
      }
    }
    stage('Start containers using docker compose'){ // https://www.youtube.com/watch?v=ZPD_PzGOvFM&t=168s (How to use docker compose with Jenkins)
      sh 'cd docker && docker compose up -d --no-color --wait' // Do I need to use sudo? If the user Jenkins is using it, perhaps not? (since I issued sudo usermod -a -G docker jenkins)
      sh 'docker compose ps'
    }
    //stage('Unit Testing') { // Perform unit testing (The tests are written based on using the home server192.168.1.157, so this won't work here)
      //steps {
        //script {
          //sh """
          //python3 -m pytest test/test_*
          //"""
        //}
      //}
    //}
    stage('Run tests against the nginx/metabase container'){
      steps{
        sh 'curl http://metabase:3000'
      }
    }
    //stage('Integration Testing') { //Perform integration testing
      //steps {
        //script {
          //sh """
          //# You have the option to stand up a temporary environment to perform
          //# these tests and/or run the tests against an existing environment. The
          //# advantage to the former is you can ensure the environment is clean
  //         # and in a desired initial state. The easiest way to stand up a temporary
  //         # environment is to use Docker and a wrapper script to orchestrate the
  //         # process. This script will handle standing up supporting services like
  //         # MySQL & Redis, running DB migrations, starting the web server, etc.
  //         # You can utilize your existing automation, your custom scripts and Make.
  //         ./standup_testing_environment.sh # Name this whatever you'd like
  //         python -m unittest discover -s tests/integration
  //       """
  //     }
  //   }
  // }  
  post {
    //failure {
      //script {
      //  msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"
        
        //slackSend message: msg, channel: env.SLACK_CHANNEL
    //}
  //}
    always{
      sh 'docker compose down --remove-orphans -v' //what is --remove-orphans
      sh 'docker compose ps'
    }
}