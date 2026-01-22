#!/usr/bin/env python3
"""
Importa canciones desde CSV de Spotify a YouTube Music Liked songs (LM)
Con reintentos y manejo de errores mejorado.
"""
import sys
import csv
import json
import time
from pathlib import Path
from ytmusicapi import YTMusic

BATCH = 50
MAX_RETRIES = 3
RETRY_DELAY = 2


def read_spotify_csv(path):
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            song = r.get('Nombre de la canción', '').strip()
            artist = r.get('Nombre(s) del artista', '').strip()
            if song:
                rows.append({'title': song, 'artist': artist})
    return rows


def search_with_retry(yt, query):
    """Busca con reintentos en caso de error"""
    for attempt in range(MAX_RETRIES):
        try:
            results = yt.search(query, filter='songs', limit=1)
            if results and results[0].get('videoId'):
                return results[0]['videoId']
            return None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return None


def main():
    csv_path = Path('1.csv')
    headers_path = Path('ytmusic_legacy.json')

    if not csv_path.exists():
        print(f'❌ No se encontró {csv_path}')
        sys.exit(1)
    
    if not headers_path.exists():
        print(f'❌ No se encontró {headers_path}')
        sys.exit(1)

    print('🔐 Autenticando con YouTube Music...')
    try:
        yt = YTMusic(auth=str(headers_path))
    except Exception as e:
        print(f'❌ Error: {e}')
        sys.exit(1)

    print('📖 Leyendo CSV de Spotify...')
    rows = read_spotify_csv(str(csv_path))
    print(f'📊 Total de canciones: {len(rows)}')

    video_ids = []
    failed = 0
    
    print('🔍 Buscando canciones en YouTube Music...')
    for i, row in enumerate(rows, start=1):
        title = row['title']
        artist = row['artist']
        query = f'{title} {artist}'.strip()
        
        if not query:
            continue
        
        # Barra de progreso cada 100
        if i % 100 == 0:
            pct = int(100 * i / len(rows))
            print(f'   [{pct:3d}%] {i}/{len(rows)}')
        
        vid = search_with_retry(yt, query)
        if vid:
            video_ids.append(vid)
        else:
            failed += 1

    print(f'\n✅ Encontradas {len(video_ids)} canciones. Fallos: {failed}.')

    if not video_ids:
        print('❌ Sin canciones para importar.')
        sys.exit(0)

    # Usar playlist automática "LM" (Liked songs)
    playlist_id = 'LM'
    print(f'\n📋 Usando playlist automática "Liked songs" (LM)...')
    print(f'   ✓ ID: {playlist_id}')

    # Añadir canciones
    print(f'\n⬆️ Añadiendo {len(video_ids)} canciones...')
    try:
        for i in range(0, len(video_ids), BATCH):
            batch = video_ids[i:i+BATCH]
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    yt.add_playlist_items(playlist_id, batch)
                    progress = min(i+BATCH, len(video_ids))
                    pct = int(100 * progress / len(video_ids))
                    print(f'   [{pct:3d}%] {progress}/{len(video_ids)}')
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count < MAX_RETRIES:
                        print(f'   ⚠️ Reintentando lote ({retry_count}/{MAX_RETRIES})...')
                        time.sleep(RETRY_DELAY)
                    else:
                        print(f'   ❌ Error al añadir lote después de {MAX_RETRIES} intentos')
                        raise
    except Exception as e:
        print(f'❌ Error fatal: {e}')
        sys.exit(1)

    print(f'\n🎉 ¡Listo! Se añadieron {len(video_ids)} canciones a tu lista "Liked songs".')
    print('📱 Abre: https://music.youtube.com/playlist?list=LM')


if __name__ == '__main__':
    main()
