#!/usr/bin/env python3
"""
Importa canciones desde CSV de Spotify a YouTube Music.
Usa YTMusic.setup() para autenticación interactiva vía navegador.
"""
import sys
import csv
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


def setup_auth():
    """Genera autenticación interactiva"""
    auth_file = Path('ytmusic_auth.json')
    if auth_file.exists():
        print('Usando autenticación guardada...')
        return YTMusic(str(auth_file))
    else:
        print('\n>>> Se abrirá tu navegador para autenticar.')
        print('>>> Por favor, inicia sesión y espera a que se complete.')
        YTMusic.setup(filepath=str(auth_file))
        return YTMusic(str(auth_file))


def main():
    csv_path = Path('1.csv')
    if not csv_path.exists():
        print(f'No se encontró {csv_path}')
        sys.exit(1)

    print('Configurando YouTube Music API...')
    yt = setup_auth()

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

    # Crear o buscar playlist
    playlist_name = 'MUSICA Q ME GUSTA'
    print(f'Buscando playlist "{playlist_name}"...')
    
    playlists = yt.get_library_playlists(limit=300)
    playlist_id = None
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

    print(f'\n✅ ¡Completado! Playlist "{playlist_name}" creada con {len(video_ids)} canciones.')
    print('Abre: https://music.youtube.com')


if __name__ == '__main__':
    main()
