pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Project Tool V1'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'V1 pipeline completed successfully!'
        }

        failure {
            echo 'V1 pipeline failed. Check the console output.'
        }
    }
}