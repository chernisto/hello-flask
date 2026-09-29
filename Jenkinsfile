pipeline {
    agent { label 'docker' }

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    environment {
        IMAGE       = 'hello-flask'
        APP_VERSION = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'docker build --target test -t ${IMAGE}:test .'
            }
        }
        stage('Build') {
            steps {
                sh '''
                    docker build --target runtime \
                      --build-arg APP_VERSION=${APP_VERSION} \
                      -t ${IMAGE}:${APP_VERSION} -t ${IMAGE}:latest .
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose -f deploy/compose.yaml -p hello-flask up -d --wait --wait-timeout 60'
            }
        }
        stage('Verify') {
            steps {
                sh '''
                    docker exec hello-flask python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').read().decode())"
                '''
            }
        }
    }

    post {
        cleanup {
            sh 'docker image prune -f || true'
            deleteDir()
        }
    }
}
