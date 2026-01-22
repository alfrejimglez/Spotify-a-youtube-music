#!/usr/bin/env python3
"""
Lista todas las playlists de tu biblioteca en YouTube Music
"""
import json
from pathlib import Path
from ytmusicapi import YTMusic

headers_path = Path('ytmusic_legacy.json')

if not headers_path.exists():
    print(f'❌ No se encontró {headers_path}')
    exit(1)

print('🔐 Conectando...')
yt = YTMusic(auth=str(headers_path))

print('\n📋 Tus playlists:\n')
playlists = yt.get_library_playlists(limit=300)

if not playlists:
    print('   (sin playlists)')
else:
    for i, p in enumerate(playlists, 1):
        name = p.get('title', '?')
        pid = p.get('playlistId', '?')
        count = p.get('count', '?')
        print(f'{i}. "{name}" | ID: {pid} | Canciones: {count}')

print('\n')
