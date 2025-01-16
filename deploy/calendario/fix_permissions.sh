#!/bin/bash

# Ajusta permissões para diretórios (755)
find . -type d -exec chmod 755 {} \;

# Ajusta permissões para arquivos (644)
find . -type f -exec chmod 644 {} \;

# Garante que os scripts Python sejam executáveis
find . -name "*.py" -exec chmod 755 {} \;

# Garante que o virtualenv/bin seja executável
if [ -d "venv/bin" ]; then
    chmod -R 755 venv/bin
fi

echo "Permissões ajustadas com sucesso!"
