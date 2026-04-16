#!/usr/bin/env python3
"""
Importa canciones desde CSV de Spotify a YouTube Music.
Usa YTMusic.setup() para autenticación interactiva vía navegador.
"""
import sys
import csv
import json
import argparse
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from ytmusicapi import YTMusic

BATCH = 50


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


def parse_args():
    parser = argparse.ArgumentParser(description='Importa CSV de Spotify a una playlist de YouTube Music')
    parser.add_argument('--csv', default='ejemplo.csv', help='Ruta al CSV exportado de Spotify')
    parser.add_argument('--auth', default='ytmusic_headers.json', help='Ruta al JSON de autenticación')
    parser.add_argument('--playlist-url', default='', help='URL completa de playlist destino')
    parser.add_argument('--playlist-id', default='', help='ID de playlist destino (ej: PLxxxx)')
    parser.add_argument('--playlist-name', default='Putos Remix', help='Nombre de playlist a buscar/crear si no se pasa URL/ID')
    return parser.parse_args()


def extract_playlist_id(playlist_url):
    try:
        parsed = urlparse(playlist_url)
        query = parse_qs(parsed.query)
        pid = query.get('list', [''])[0]
        return pid.strip()
    except Exception:
        return ''


def setup_auth(auth_path):
    """Autenticación desde ytmusic_headers.json o formato legacy"""
    if not auth_path.exists():
        print(f'No se encontró {auth_path}')
        sys.exit(1)

    with open(auth_path, 'r', encoding='utf-8') as f:
        auth_data = json.load(f)

    if isinstance(auth_data, dict) and 'headers' in auth_data:
        print('Usando autenticación desde campo "headers"...')
        return YTMusic(auth=auth_data['headers'])

    print('Usando autenticación legacy desde archivo...')
    return YTMusic(auth=str(auth_path))


def main():
    args = parse_args()
    csv_path = Path(args.csv)
    auth_path = Path(args.auth)

    if not csv_path.exists():
        print(f'No se encontró {csv_path}')
        sys.exit(1)

    print('Configurando YouTube Music API...')
    yt = setup_auth(auth_path)

    print('Leyendo CSV de Spotify...')
    rows = read_spotify_csv(str(csv_path))
    print(f'Total de canciones: {len(rows)}')

    video_ids = []
    failed = 0
    
    for i, row in enumerate(rows, start=1):
        title = row['title']
        artist = row['artist']
        query = f'{title} {artist}'.strip()
        
        if not query:
            continue
        
        if i % 100 == 0:
            print(f'  {i}/{len(rows)}: procesadas...')
        
        try:
            results = yt.search(query, filter='songs', limit=1)
            if results and results[0].get('videoId'):
                video_ids.append(results[0]['videoId'])
            else:
                failed += 1
        except Exception as e:
            failed += 1

    print(f'Encontradas {len(video_ids)} canciones. Fallos: {failed}.')

    if not video_ids:
        print('Sin canciones para importar.')
        sys.exit(0)

    # Elegir playlist destino
    playlist_id = args.playlist_id.strip() or extract_playlist_id(args.playlist_url.strip())
    playlist_name = args.playlist_name.strip()

    if playlist_id:
        print(f'Usando playlist destino ID: {playlist_id}')
    else:
        print(f'Buscando playlist "{playlist_name}"...')
        playlists = yt.get_library_playlists(limit=300)
        for p in playlists:
            if p.get('title') == playlist_name:
                playlist_id = p.get('playlistId')
                print(f'Encontrada: {playlist_id}')
                break

        if not playlist_id:
            print(f'Creando playlist "{playlist_name}"...')
            playlist_id = yt.create_playlist(playlist_name, 'Importada desde Spotify CSV')
            print(f'Creada: {playlist_id}')

    # Añadir canciones
    print(f'Añadiendo {len(video_ids)} canciones...')
    for i in range(0, len(video_ids), BATCH):
        batch = video_ids[i:i+BATCH]
        yt.add_playlist_items(playlist_id, batch)
        print(f'  ✓ {min(i+BATCH, len(video_ids))}/{len(video_ids)}')

    print(f'\n✅ ¡Completado! Añadidas {len(video_ids)} canciones a la playlist {playlist_id}.')
    print('Abre: https://music.youtube.com')


if __name__ == '__main__':
    main()
