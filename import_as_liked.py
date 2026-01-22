#!/usr/bin/env python3
"""
Importa canciones desde CSV de Spotify a YouTube Music "Liked songs"
Marca cada canción como "liked" (👍) en lugar de usar playlist.
"""
import sys
import csv
import json
import time
from pathlib import Path
from ytmusicapi import YTMusic

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
                return results[0]
            return None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return None


def rate_song_with_retry(yt, video_id):
    """Marca canción como liked con reintentos"""
    for attempt in range(MAX_RETRIES):
        try:
            yt.rate_song(video_id, 'LIKE')
            return True
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return False


def main():
    csv_path = Path('1.csv')
    headers_path = Path('ytmusic_headers.json')

    if not csv_path.exists():
        print(f'❌ No se encontró {csv_path}')
        sys.exit(1)
    
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

    print('📖 Leyendo CSV de Spotify...')
    rows = read_spotify_csv(str(csv_path))
    rows.reverse()  # Invertir orden para que las viejas queden primero
    print(f'📊 Total de canciones: {len(rows)}')

    liked_count = 0
    failed = 0
    
    print('🔍 Buscando y marcando como "liked" en YouTube Music...')
    for i, row in enumerate(rows, start=1):
        title = row['title']
        artist = row['artist']
        query = f'{title} {artist}'.strip()
        
        if not query:
            continue
        
        # Barra de progreso cada 50
        if i % 50 == 0:
            pct = int(100 * i / len(rows))
            print(f'   [{pct:3d}%] {i}/{len(rows)} | Marcadas: {liked_count}')
        
        song = search_with_retry(yt, query)
        if song:
            video_id = song.get('videoId')
            if video_id:
                if rate_song_with_retry(yt, video_id):
                    liked_count += 1
                else:
                    failed += 1
            else:
                failed += 1
        else:
            failed += 1

    print(f'\n✅ Completado:')
    print(f'   • Marcadas como "liked": {liked_count}')
    print(f'   • Fallos: {failed}')
    print(f'   • Total: {len(rows)}')

    print(f'\n🎉 ¡Listo! {liked_count} canciones ahora están en tu lista "Música que me gusta".')
    print('📱 Abre: https://music.youtube.com/playlist?list=LM')


if __name__ == '__main__':
    main()
