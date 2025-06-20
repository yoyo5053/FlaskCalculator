pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        bat """
          REM Installe toutes les dépendances avec le python absolu
          "C:\\Users\\km\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install Flask Flask-RESTx Loguru pytest pytest-cov pytest-flask
        """
      }
    }

    stage('Run tests') {
      steps {
        bat """
          REM Prépare le dossier results
          if exist results rmdir /s /q results
          mkdir results

          REM Exécute pytest via l'exécutable Python absolu
          "C:\\Users\\km\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest Tests --junitxml=results\\report.xml ^
                                                                                   --cov=main --cov-report=xml:results\\coverage.xml ^
                                                                                   --cov-report=html:results\\htmlcov
        """
      }
    }
  }

  post {
    always {
      junit 'results\\report.xml'
      cobertura coberturaReportFile: 'results\\coverage.xml'
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
