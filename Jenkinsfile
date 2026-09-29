pipeline {
    // No global agent: the approval stage waits WITHOUT holding the Pi's only executor.
    agent none

    options {
        timeout(time: 2, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // A newer push aborts an older build still waiting for approval.
        disableConcurrentBuilds(abortPrevious: true)
    }

    environment {
        IMAGE       = 'hello-flask'
        APP_VERSION = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Test & Build') {
            agent { label 'docker' }
            steps {
                sh 'docker build --target test -t ${IMAGE}:test .'
                // Build ONCE. The same image tag is promoted to staging and production.
                sh '''
                    docker build --target runtime \
                      --build-arg APP_VERSION=${APP_VERSION} \
                      -t ${IMAGE}:${APP_VERSION} .
                '''
            }
            post { cleanup { deleteDir() } }
        }

        stage('Deploy to staging') {
            agent { label 'docker' }
            environment {
                ENV_NAME  = 'staging'
                HOST_PORT = '8083'
            }
            steps {
                sh 'docker compose -f deploy/compose.yaml -p hello-flask-${ENV_NAME} up -d --wait --wait-timeout 60'
                sh '''docker exec hello-flask-${ENV_NAME} python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').read().decode())"'''
            }
            post { cleanup { deleteDir() } }
        }

        stage('Approve production') {
            // Runs on no node: waiting costs nothing.
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    input message: "Promote build ${env.BUILD_NUMBER} (tested on staging) to production?",
                          ok: 'Deploy to production',
                          submitter: 'jenkins-admins'
                }
            }
        }

        stage('Deploy to production') {
            agent { label 'docker' }
            environment {
                ENV_NAME  = 'production'
                HOST_PORT = '8082'
            }
            steps {
                sh 'docker compose -f deploy/compose.yaml -p hello-flask-${ENV_NAME} up -d --wait --wait-timeout 60'
                sh '''docker exec hello-flask-${ENV_NAME} python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').read().decode())"'''
            }
            post { cleanup { deleteDir() } }
        }
    }
}