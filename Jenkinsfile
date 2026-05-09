pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        ALLURE_RESULTS = 'reports/allure-results'
        ALLURE_REPORT = 'reports/allure-report'
        TEST_USERNAME = '18162428572'
        TEST_PASSWORD = '111111'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install chromium
                '''
            }
        }

        stage('Clean Results') {
            steps {
                sh '''
                    echo "Cleaning previous Allure results..."
                    rm -rf ${ALLURE_RESULTS}/*
                    echo "Directory contents after cleanup:"
                    ls -la ${ALLURE_RESULTS} 2>/dev/null || echo "Directory empty or does not exist"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -o "addopts=" --browser=chromium --alluredir=${ALLURE_RESULTS} -v
                    echo "=== Allure results verification ==="
                    ls -la ${ALLURE_RESULTS} || echo "WARNING: Allure results directory not found!"
                '''
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
