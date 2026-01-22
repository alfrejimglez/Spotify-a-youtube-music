# YouTube Music Importer desde Spotify

Suite de scripts Python para importar canciones de Spotify a YouTube Music.

---

## 📋 Scripts incluidos

### 1. `import_final.py`
Importa canciones desde un CSV de Spotify a una playlist personalizada en YouTube Music.
EL CSV se puede generar de https://exportify.app/ 
**Qué hace:**
- Lee un CSV de Spotify con títulos y artistas
- Busca cada canción en YouTube Music
- Crea una playlist (o usa una existente) llamada "spotify"
- Añade todas las canciones encontradas a esa playlist

**Uso:**
```bash
python import_final.py
```

**Requisitos previos:**
- Archivo `1.csv` (exportado desde Spotify)
- Archivo `ytmusic_legacy.json` (credenciales de YouTube Music)
- Librería `ytmusicapi` instalada

**Tiempo estimado:** 30-60 minutos (según número de canciones)

**Resultado:** Playlist llamada "spotify" con las canciones importadas

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

### 2. Obtener credenciales (`ytmusic_legacy.json`)

**Opción A: Desde `headers_auth.json` (recomendado)**

1. Instala la extensión **"Get YTMusic headers"** en Chrome/Edge
2. Abre https://music.youtube.com
3. Haz clic en la extensión y descarga `headers_auth.json`
4. Coloca el archivo en la carpeta de scripts
5. Ejecuta este comando Python para convertirlo:

```python
import json
from pathlib import Path

with open('headers_auth.json') as f:
    data = json.load(f)

legacy = {
    'Accept': '*/*',
    'Authorization': data['headers'].get('Authorization', ''),
    'Content-Type': 'application/json',
    'Cookie': data['headers'].get('Cookie', ''),
    'User-Agent': 'Mozilla/5.0',
    'X-Goog-AuthUser': '0',
    'x-origin': 'https://music.youtube.com'
}

with open('ytmusic_legacy.json', 'w') as f:
    json.dump(legacy, f, indent=2)

print('✓ ytmusic_legacy.json creado')
```

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
├── import_final.py
├── list_playlists.py
├── import_as_liked.py
├── 1.csv                    (tu CSV de Spotify)
├── ytmusic_legacy.json      (credenciales YouTube Music)
└── README.md                (este archivo)
```

---

## 🚀 Ejemplos de uso

### Caso 1: Importar a playlist personalizada "spotify"
```bash
python import_final.py
```
→ Crea o reutiliza playlist llamada "spotify"

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

### Error: "No se encontró `1.csv`"
→ Asegúrate de que el archivo está en la misma carpeta que los scripts

### Error: "No se encontró `ytmusic_legacy.json`"
→ Ejecuta el paso de configuración inicial para generar el archivo

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
- Las credenciales (`ytmusic_legacy.json`) **no son privadas en el sentido absoluto** — guárdalo seguro

---

## 🔗 Enlaces útiles

- **YouTube Music:** https://music.youtube.com
- **Mis playlists:** https://music.youtube.com/library/playlists
- **Música que me gusta (LM):** https://music.youtube.com/playlist?list=LM
- **Documentación ytmusicapi:** https://ytmusicapi.readthedocs.io/

---

**Última actualización:** 22 de enero de 2026
