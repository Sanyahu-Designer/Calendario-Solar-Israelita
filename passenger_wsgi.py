import os
import sys

# Adiciona o diretório do projeto ao path do Python
sys.path.insert(0, os.path.dirname(__file__))

# Define as variáveis de ambiente
os.environ['DJANGO_SETTINGS_MODULE'] = 'calendario_solar.settings'

# Importa a aplicação WSGI do Django
from calendario_solar.wsgi import application
