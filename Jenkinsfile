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
          REM Crée et active le venv
          python -m venv venv
          call venv\\Scripts\\activate.bat

          REM Installe les dépendances
          pip install -r requirements.txt
        """
      }
    }

    stage('Run tests') {
      steps {
        bat """
          REM Active le venv
          call venv\\Scripts\\activate.bat

          REM Prépare le dossier results
          if exist results rmdir /s /q results
          mkdir results

          REM Lance pytest et génère JUnit + Cobertura + HTMLcov
          pytest --junitxml=results\\report.xml ^
                 --cov=calculator --cov-report=xml:results\\coverage.xml ^
                 --cov-report=html:results\\htmlcov
        """
      }
    }
  }

  post {
    always {
      // Archive les résultats JUnit
      junit 'results\\report.xml'
      // Archive la couverture Cobertura
      cobertura coberturaReportFile: 'results\\coverage.xml'
      // Archive le rapport HTML pour le visualiser
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
