import os
import sys
import django
from decouple import config

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendario_solar.settings')
django.setup()

# Importar depois de configurar o Django
from django.db import connections
from django.db.utils import OperationalError

try:
    conn = connections['default']
    conn.cursor()
    print("Conexão com o banco de dados bem sucedida!")
    
    # Imprimir as configurações do banco de dados (sem a senha)
    print("\nConfigurações do banco de dados:")
    print(f"NAME: {config('DB_NAME', 'calendario')}")
    print(f"USER: {config('DB_USER', 'root')}")
    print(f"HOST: {config('DB_HOST', 'localhost')}")
    print(f"PORT: {config('DB_PORT', '3306')}")
    
except OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
