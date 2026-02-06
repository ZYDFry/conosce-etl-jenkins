pipeline {
    agent any
    triggers {
        // H/2 significa: "Revisar cambios cada 2 minutos aprox"
        cron 'H/2 * * * *' 
    }

    stages {
        // --- PASO 0: PREPARACIÓN ---
        stage('Preparar Entorno') {
            steps {
                echo 'Verificando librerías necesarias...'
                // Instalamos pandas y openpyxl (solo si faltan)
                bat '"C:\\Users\\ZYDF\\AppData\\Local\\Python\\bin\\python.exe" -m pip install pandas openpyxl'
            }
        }
        
        // --- PASO 1: LECTURA (EXTRACT) ---
        stage('1. Extracción (READ)') {
            steps {
                echo 'Iniciando lectura de archivos Excel...'
                // Ejecuta el script que Jenkins descargó de GitHub
                bat '"C:\\Users\\ZYDF\\AppData\\Local\\Python\\bin\\python.exe" data_read.py'
            }
        }
            
        // --- PASO 2: TRANSFORMACIÓN (TRANSFORM) ---
        stage('2. Transformación (TRANSFORM)') {
            steps {
                echo 'Aplicando filtros y limpieza de datos...'
                bat '"C:\\Users\\ZYDF\\AppData\\Local\\Python\\bin\\python.exe" data_transform.py'
            }
        }

        // --- PASO 3: CARGA / EXPORTACIÓN (LOAD) ---
        stage('3. Exportación (LOAD)') {
            steps {
                echo 'Generando reporte Excel final...'
                bat '"C:\\Users\\ZYDF\\AppData\\Local\\Python\\bin\\python.exe" data_export.py'
            }
        }

        // --- PASO 4: NOTIFICACIÓN (MAIL) ---
        stage('4. Notificación (MAIL)') {
            steps {
                echo 'Enviando alerta de finalización...'
                bat '"C:\\Users\\ZYDF\\AppData\\Local\\Python\\bin\\python.exe" data_notify.py'
            }
        }
    }
    
    post {
        success {
            echo "PIPELINE EXITOSO. Revisa la carpeta 'Resultados' en el Workspace."
        }
        failure {
            echo "FALLO EN EL PROCESO. Revisa qué etapa (Stage) se puso roja arriba."
        }
    }
}