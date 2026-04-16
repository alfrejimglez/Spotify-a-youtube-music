#!/usr/bin/env python3
"""
Quita el like a TODAS las canciones de "Música que me gusta"
Úsalo para limpiar antes de reimportar con el orden correcto.
"""
import sys
import json
import time
from pathlib import Path
from ytmusicapi import YTMusic

MAX_RETRIES = 3
RETRY_DELAY = 2


def unlike_with_retry(yt, video_id):
    """Quita like de una canción con reintentos"""
    for attempt in range(MAX_RETRIES):
        try:
            yt.rate_song(video_id, 'INDIFFERENT')
            return True
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return False


def main():
    headers_path = Path('ytmusic_headers.json')

    if not headers_path.exists():
        print(f'❌ No se encontró {headers_path}')
        sys.exit(1)

    print('🔐 Autenticando con YouTube Music...')
    try:
        # Cargar headers desde el JSON
        with open(headers_path, 'r') as f:
            auth_data = json.load(f)
        
        # Si es el nuevo formato, usar headers
        if 'headers' in auth_data:
            yt = YTMusic(auth=auth_data['headers'])
        else:
            # Si es formato antiguo, usar directamente
            yt = YTMusic(auth=str(headers_path))
    except Exception as e:
        print(f'❌ Error: {e}')
        sys.exit(1)

    print('📥 Obteniendo todas las canciones de "Música que me gusta"...')
    try:
        all_songs = []
        page = 1
        
        # Obtener canciones en bloques de 500
        while True:
            offset = (page - 1) * 500
            print(f'   📄 Página {page}: obteniendo canciones ({offset}-{offset+500})...')
            try:
                liked_songs = yt.get_liked_songs(limit=500)
                tracks = liked_songs.get('tracks', [])
                
                if not tracks:
                    break
                    
                all_songs.extend(tracks)
                
                # Si no hay continuations, paramos
                if 'continuations' not in liked_songs:
                    break
                    
                # Continuar con el siguiente lote
                continuation = liked_songs.get('continuations')[0]
                liked_songs = yt.get_liked_songs(limit=500, continuations=[continuation])
                page += 1
            except Exception as e:
                print(f'   ⚠️  Error en página {page}: {e}')
                break
        
        songs = all_songs
        print(f'📊 Total de canciones con like: {len(songs)}')
    except Exception as e:
        print(f'❌ Error al obtener canciones: {e}')
        sys.exit(1)

    if not songs:
        print('✅ No hay canciones para quitar like')
        return

    print('\n⚠️  Esto quitará like a TODAS las canciones.')
    confirm = input('¿Continuar? (s/n): ').strip().lower()
    if confirm != 's':
        print('❌ Cancelado')
        sys.exit(0)

    unlike_count = 0
    failed = 0

    print(f'\n🔄 Quitando likes...')
    for i, song in enumerate(songs, start=1):
        video_id = song.get('videoId')
        if video_id:
            if unlike_with_retry(yt, video_id):
                unlike_count += 1
            else:
                failed += 1

        # Barra de progreso cada 50
        if i % 50 == 0:
            pct = int(100 * i / len(songs))
            print(f'   [{pct:3d}%] {i}/{len(songs)} | Quitados: {unlike_count}')

    print(f'\n✅ Completado:')
    print(f'   • Like quitados: {unlike_count}')
    print(f'   • Fallos: {failed}')
    print(f'   • Total: {len(songs)}')
    print(f'\n🎉 ¡Listo! Ahora puedes reimportar con el script correcto.')


if __name__ == '__main__':
    main()
