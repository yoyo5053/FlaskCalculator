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
          REM Crée un virtualenv avec le launcher py
          py -3 -m venv venv
          
          REM Active le venv
          call venv\\Scripts\\activate.bat
          
          REM Installe les dépendances du projet
          pip install -r requirements.txt
        """
      }
    }

    stage('Run tests') {
      steps {
        bat """
          REM Active le venv
          call venv\\Scripts\\activate.bat

          REM Reconstruit le dossier results
          if exist results rmdir /s /q results
          mkdir results

          REM Lance pytest et génère les rapports
          pytest --junitxml=results\\report.xml ^
                 --cov=calculator --cov-report=xml:results\\coverage.xml ^
                 --cov-report=html:results\\htmlcov
        """
      }
    }
  }

  post {
    always {
      // Publie les résultats JUnit
      junit 'results\\report.xml'
      // Publie la couverture Cobertura
      cobertura coberturaReportFile: 'results\\coverage.xml'
      // Archive le rapport HTML 
      archiveArtifacts artifacts: 'results/htmlcov/**', fingerprint: true
    }
  }
}
