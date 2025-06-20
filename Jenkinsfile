pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        // clone & checkout de la branche paramétrée dans le job
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        bat """
          REM Installe Flask, RESTx, Loguru + pytest et extensions
          py -3 -m pip install Flask Flask-RESTx Loguru
          py -3 -m pip install pytest pytest-cov pytest-flask
        """
      }
    }

    stage('Run tests') {
      steps {
        bat """
          REM Crée le répertoire results
          if exist results rmdir /s /q results
          mkdir results

          REM Lance pytest sur le dossier Tests/ (où sont tes tests)
          py -3 -m pytest Tests --junitxml=results\\report.xml ^
                                  --cov=main --cov-report=xml:results\\coverage.xml ^
                                  --cov-report=html:results\\htmlcov
        """
      }
    }
  }

  post {
    always {
      // Archives JUnit / Cobertura / HTMLcov
      junit 'results\\report.xml'
      cobertura coberturaReportFile: 'results\\coverage.xml'
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
