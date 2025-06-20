pipeline {
  agent any
  tools { python 'Python3' }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install') {
      steps {
        sh '''
          python -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
        '''
      }
    }
    stage('Tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest --junitxml=results/report.xml \
                 --cov=calculator --cov-report=xml:results/coverage.xml \
                 --cov-report=html:results/htmlcov
        '''
      }
    }
  }
  post {
    always {
      junit 'results/report.xml'
      cobertura coberturaReportFile: 'results/coverage.xml'
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
