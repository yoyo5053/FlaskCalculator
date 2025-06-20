pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        // Clone le dépôt configuré dans le job
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        // Crée et active un virtualenv, puis installe les dépendances
        sh '''
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run tests') {
      steps {
        // Lance pytest en générant JUnit, Cobertura et HTMLcov
        sh '''
          source venv/bin/activate
          pytest --junitxml=results/report.xml \
                 --cov=calculator --cov-report=xml:results/coverage.xml \
                 --cov-report=html:results/htmlcov
        '''
      }
    }
  }

  post {
    always {
      // Publie les résultats JUnit et la couverture Cobertura
      junit 'results/report.xml'
      cobertura coberturaReportFile: 'results/coverage.xml'
      // Archive le rapport HTML pour pouvoir le télécharger/viewer dans Jenkins
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
