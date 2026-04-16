# YouTube Music Importer desde Spotify

Suite de scripts Python para importar canciones de Spotify a YouTube Music.

---
📋EL CSV se puede generar de https://exportify.app/ 📋
Las headers o manualmente (requests headers) o con extensiones como https://chromewebstore.google.com/detail/yt-music-header-exporter/khjdlndhcgibldagopmlbdbhjejinlpo

## 📋 Scripts incluidos

### 1. `import_simple.py`
Importa canciones desde un CSV de Spotify a una playlist concreta de YouTube Music.

**Qué hace:**
- Lee un CSV de Spotify con títulos y artistas
- Busca cada canción en YouTube Music
- Permite elegir playlist por URL, por ID o por nombre
- Crea la playlist si no existe (cuando usas nombre)
- Añade todas las canciones encontradas a esa playlist

**Uso:**
```bash
python import_simple.py --csv putos_remix.csv --auth ytmusic_headers.json --playlist-url "https://music.youtube.com/playlist?list=PLwMPz54iutsizG6ssq4kjvLRSYiWuaxhx"
```

**Si lo ejecutas sin parámetros:**
```bash
python import_simple.py
```
El script usa estos valores por defecto:
- `--csv ejemplo.csv`
- `--auth ytmusic_headers.json`
- `--playlist-name "Putos Remix"` (solo si no pasas `--playlist-url` ni `--playlist-id`)

En ese modo, buscará `ejemplo.csv`; si no existe, terminará con error de archivo no encontrado.

**Parámetros disponibles:**
- `--csv` Ruta del CSV (por defecto: `ejemplo.csv`)
- `--auth` Ruta del JSON de auth (`ytmusic_headers.json` o formato legacy)
- `--playlist-url` URL completa de la playlist destino
- `--playlist-id` ID de playlist destino (ej: `PL...`)
- `--playlist-name` Nombre de playlist a buscar/crear (si no pasas URL/ID)

**Requisitos previos:**
- Archivo CSV exportado desde Spotify (ej: `putos_remix.csv`)
- Archivo `ytmusic_headers.json` (credenciales de YouTube Music)
- Librería `ytmusicapi` instalada

**Tiempo estimado:** 30-60 minutos (según número de canciones)

**Resultado:** Canciones añadidas a la playlist que indiques

---

### 2. `list_playlists.py`
Lista todas tus playlists en YouTube Music con ID y número de canciones.

**Qué hace:**
- Conecta a tu cuenta de YouTube Music
- Muestra todas tus playlists personalizadas
- Muestra el ID de cada playlist (útil para referencia)
- Muestra cantidad de canciones

**Uso:**
```bash
python list_playlists.py
```

**Requisitos previos:**
- Archivo `ytmusic_legacy.json`
- Librería `ytmusicapi` instalada

**Tiempo estimado:** 5 segundos

**Salida de ejemplo:**
```
📋 Tus playlists:

1. "Liked Music" | ID: LM | Canciones: ?
2. "spotify" | ID: PLwMPz54iutsgnSVPUl0tILHOmo9BeQF0s | Canciones: 650
3. "Episodes for Later" | ID: SE | Canciones: ?
```

---

### 3. `import_as_liked.py`
Marca cada canción del CSV como "liked" (👍) para añadirlas a tu lista automática "Música que me gusta".

**Qué hace:**
- Lee un CSV de Spotify con títulos y artistas
- Busca cada canción en YouTube Music
- Marca cada una como "liked" usando el botón 👍
- Las canciones se añaden automáticamente a la lista "Música que me gusta" (LM)

**Uso:**
```bash
python import_as_liked.py
```

**Requisitos previos:**
- Archivo `1.csv` (exportado desde Spotify)
- Archivo `ytmusic_legacy.json`
- Librería `ytmusicapi` instalada

**Tiempo estimado:** 40-90 minutos (según número de canciones)

**Resultado:** Todas las canciones en tu lista "Música que me gusta" (https://music.youtube.com/playlist?list=LM)

---

## 🔧 Configuración inicial

### 1. Instalar requisitos
```bash
python -m pip install ytmusicapi requests
```

### 2. Obtener credenciales (`ytmusic_headers.json`)

**Opción A: Desde `headers_auth.json` (recomendado)**

1. Instala la extensión **"Get YTMusic headers"** en Chrome/Edge
2. Abre https://music.youtube.com
3. Haz clic en la extensión y descarga `headers_auth.json`
4. Coloca el archivo en la carpeta de scripts
5. Guárdalo como `ytmusic_headers.json` en la carpeta del proyecto

### 3. Obtener CSV de Spotify

1. Abre https://www.spotify.com
2. Ve a tu biblioteca → "Canciones Guardadas"
3. Haz clic derecho → "Descargar" (o usa exportador externo como TuneMyMusic)
4. Guarda como `1.csv`
5. Coloca en la misma carpeta que los scripts

---

## 📁 Estructura de archivos

```
carpeta_scripts/
├── import_simple.py
├── list_playlists.py
├── import_as_liked.py
├── putos_remix.csv          (tu CSV de Spotify)
├── ytmusic_headers.json     (credenciales YouTube Music)
└── README.md                (este archivo)
```

---

## 🚀 Ejemplos de uso

### Caso 1: Importar a una playlist por URL
```bash
python import_simple.py --csv putos_remix.csv --auth ytmusic_headers.json --playlist-url "https://music.youtube.com/playlist?list=PLwMPz54iutsizG6ssq4kjvLRSYiWuaxhx"
```
→ Añade canciones a esa playlist exacta

### Caso 1B: Importar por ID de playlist
```bash
python import_simple.py --csv putos_remix.csv --auth ytmusic_headers.json --playlist-id PLwMPz54iutsizG6ssq4kjvLRSYiWuaxhx
```
→ Añade canciones a la playlist indicada por ID

### Caso 1C: Importar por nombre de playlist
```bash
python import_simple.py --csv putos_remix.csv --auth ytmusic_headers.json --playlist-name "Putos Remix"
```
→ Busca por nombre y la crea si no existe

### Caso 2: Ver tus playlists actuales
```bash
python list_playlists.py
```
→ Lista todas tus playlists con IDs

### Caso 3: Marcar como "liked" para lista automática
```bash
python import_as_liked.py
```
→ Añade a "Música que me gusta" (LM)

---

## ⚙️ Características técnicas

- **Búsqueda inteligente:** Busca por título + artista para máxima precisión
- **Reintentos automáticos:** Si falla una búsqueda, reintentas 3 veces
- **Barra de progreso:** Actualiza cada 50-100 canciones
- **Manejo de errores:** Muestra fallos sin detener la ejecución

---

## ⚠️ Limitaciones conocidas

- **YouTube Music no tiene exactamente todas las canciones:** Algunas pueden no encontrarse
- **Límite de API:** Si tienes >10.000 canciones, puede haber throttling
- **Duplicados:** Si importas 2 veces, habrá duplicados (no verifica automáticamente)
- **Tiempo:** Cada canción tarda 2-5 segundos en buscarse y procesarse

---

## 🆘 Solución de problemas

### Error: "No se encontró `ejemplo.csv` o tu CSV"
→ Asegúrate de que el archivo está en la misma carpeta que los scripts

### Error: "No se encontró `ytmusic_headers.json`"
→ Exporta de nuevo headers/cookies y guarda el archivo con ese nombre

### Error: "ModuleNotFoundError: No module named 'ytmusicapi'"
→ Instala: `python -m pip install ytmusicapi`

### El script es muy lento
→ Normal. YouTube Music limita requests. No aceleres demasiado.

### Se detiene sin terminar
→ Internet inestable o YouTube Music rechazó la conexión. Reinicia.

---

## 📝 Notas

- Los scripts son **seguros**: solo leen y modifican tu biblioteca
- **No borran nada** automáticamente
- Puedes **ejecutarlos varias veces** sin problemas (crea/reutiliza playlists)
- Las credenciales (`ytmusic_headers.json`) **no son privadas en el sentido absoluto** — guárdalo seguro

---

## 🔗 Enlaces útiles

- **YouTube Music:** https://music.youtube.com
- **Mis playlists:** https://music.youtube.com/library/playlists
- **Música que me gusta (LM):** https://music.youtube.com/playlist?list=LM
- **Documentación ytmusicapi:** https://ytmusicapi.readthedocs.io/

---

**Última actualización:** 18 de febrero de 2026

