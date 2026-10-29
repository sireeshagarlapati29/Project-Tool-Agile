pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\siree\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Project Tool V2'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '"%PYTHON%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'V2 pipeline completed successfully!'
        }
        failure {
            echo 'V2 pipeline failed. Check the console output.'
        }
    }
}