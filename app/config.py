# config.py

import os
from dotenv import load_dotenv

# Cargar variables del archivo .env (Para pruebas de codigo remoto sin contenedor)
load_dotenv()

# Constantes configurables desde entorno o valores por defecto
MAX_UPLOAD_SIZE = 32 * 1024 * 1024
VT_BASE_URL = "https://www.virustotal.com/api/v3"
MAX_WAIT_SECONDS = 300
VT_API_KEY = os.getenv("VT_API_KEY")
