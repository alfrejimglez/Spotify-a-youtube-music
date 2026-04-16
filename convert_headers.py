#!/usr/bin/env python3
"""
Extrae y convierte headers_auth.json a formato ytmusicapi.
"""
import json
from pathlib import Path

headers_file = Path('\\\\chuimi-nas-user\\Docs$\\ext-ajimgon\\Downloads\\headers_auth.json')
output_file = Path('\\\\chuimi-nas-user\\Docs$\\ext-ajimgon\\Downloads\\ytmusic_headers.json')

with open(headers_file) as f:
    data = json.load(f)

# Extraer cabeceras y cookies
headers = data.get('headers', {})
cookies = data.get('cookies', [])

# Construir formato ytmusicapi
ytmusic_data = {
    'headers': headers,
    'cookies': cookies
}

output_file.write_text(json.dumps(ytmusic_data, indent=2))
print(f'Archivo convertido: {output_file}')
print('Contenido:')
print(json.dumps(ytmusic_data, indent=2)[:500])
