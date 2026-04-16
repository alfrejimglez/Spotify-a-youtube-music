#!/usr/bin/env python3
"""
Importa canciones desde CSV de Spotify a playlist de YouTube Music.
Usa headers_auth.json con cabeceras de autenticación.
"""
import sys
import csv
import json
import requests
from pathlib import Path
from urllib.parse import urlencode

BATCH = 50


def read_spotify_csv(path):
    """Lee CSV de Spotify con columnas: Nombre de la canción, Nombre(s) del artista"""
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            song_name = r.get('Nombre de la canción', '').strip()
            artists = r.get('Nombre(s) del artista', '').strip()
            if song_name or artists:
                rows.append({'title': song_name, 'artist': artists})
    return rows


def search_youtube_music(headers, query):
    """Busca canciones en YouTube Music usando API interna"""
    try:
        url = 'https://music.youtube.com/youtubei/v1/search'
        params = {'key': 'AIzaSyC9V_BSILMW91dq4z7qDCta3iq_4RjJiS'}
        
        data = {
            'context': {
                'client': {
                    'clientName': 'WEB_REMIX',
                    'clientVersion': '1.0'
                }
            },
            'query': query
        }
        
        response = requests.post(url, json=data, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            result = response.json()
            # Buscar en resultados de canciones
            try:
                contents = result['contents']['tabbedSearchResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
                for section in contents:
                    if 'musicShelfRenderer' in section:
                        items = section['musicShelfRenderer'].get('contents', [])
                        for item in items:
                            if 'musicResponsiveListItemRenderer' in item:
                                overlay = item['musicResponsiveListItemRenderer'].get('overlay', {})
                                if 'musicPlayButtonRenderer' in overlay:
                                    vid = overlay['musicPlayButtonRenderer'].get('playNavigationEndpoint', {}).get('watchPlaylistEndpoint', {}).get('playlistId')
                                    if vid:
                                        return vid
            except:
                pass
        return None
    except Exception as e:
        return None


def main():
    csv_path = Path('\\\\chuimi-nas-user\\Docs$\\ext-ajimgon\\Downloads\\1.csv')
    headers_path = Path('\\\\chuimi-nas-user\\Docs$\\ext-ajimgon\\Downloads\\headers_auth.json')
    playlist_name = 'MUSICA Q ME GUSTA'

    if not csv_path.exists():
        print(f'No se encontró: {csv_path}')
        sys.exit(1)
    
    if not headers_path.exists():
        print(f'No se encontró: {headers_path}')
        sys.exit(1)

    print('Cargando cabeceras de autenticación...')
    with open(str(headers_path)) as f:
        headers_data = json.load(f)
    
    headers = headers_data.get('headers', {})
    if not headers:
        print('No se encontraron cabeceras en headers_auth.json')
        sys.exit(1)

    print('Leyendo CSV de Spotify...')
    rows = read_spotify_csv(str(csv_path))
    print(f'Total de canciones: {len(rows)}')

    print('\n⚠️ Nota: La búsqueda manual es lenta. Instalando ytmusicapi con autenticación alternativa...\n')
    
    # Intenta usar ytmusicapi con headless_browser si está disponible
    try:
        from ytmusicapi import YTMusic
        # Generar oauth manual desde headers
        oauth_file = Path('oauth.json')
        oauth_file.write_text(json.dumps({
            'client_id': '',
            'client_secret': '',
            'refresh_token': headers.get('Authorization', '')
        }))
        yt = YTMusic(oauth_credentials=str(oauth_file))
        print('YTMusic inicializado correctamente')
    except:
        print('No se pudo iniciar YTMusic. Contacta con soporte.')
        sys.exit(1)


if __name__ == '__main__':
    main()

