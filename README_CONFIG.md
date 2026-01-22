# YouTube Music Configuration Files

Este directorio contiene archivos de configuración de ejemplo para trabajar con YouTube Music API.

## Archivos de Configuración

### ytmusic_cookies.json.example
Contiene la lista de cookies necesarias para autenticar con YouTube Music.

**Cómo usar:**
1. Copia este archivo y renómbralo a `ytmusic_cookies.json`
2. Reemplaza los valores `YOUR_*` con tus cookies reales
3. Extrae las cookies de tu navegador usando las DevTools (F12) → Application → Cookies

### ytmusic_headers.json.example
Headers HTTP junto con la lista de cookies necesarias para las solicitudes.

**Cómo usar:**
1. Copia este archivo y renómbralo a `ytmusic_headers.json`
2. Reemplaza los valores `YOUR_*` con tus valores reales
3. Actualiza especialmente el header `Authorization` con tu token SAPISID

### ytmusic_legacy.json.example
Formato heredado de headers simplificado (sin estructura de objeto anidado).

**Cómo usar:**
1. Copia este archivo y renómbralo a `ytmusic_legacy.json`
2. Reemplaza los valores según sea necesario

### headers_auth.json.example
Archivo de autenticación completo con versión y timestamps.

**Cómo usar:**
1. Copia este archivo y renómbralo a `headers_auth.json`
2. Reemplaza todos los valores `YOUR_*` con tus datos reales
3. Actualiza `capturedAt` con la fecha actual si es necesario

## Cómo Obtener tus Credenciales

### Método 1: Extrae desde el navegador
1. Abre https://music.youtube.com/
2. Abre las DevTools (F12)
3. Ve a **Application** → **Cookies** → youtube.com
4. Copia los valores que necesitas reemplazar en los archivos

### Método 2: Desde Network Tab
1. Abre las DevTools (F12)
2. Ve a la pestaña **Network**
3. Realiza una acción en YouTube Music (buscar, reproducir, etc.)
4. Haz clic en una solicitud
5. Copia los headers necesarios

## ⚠️ ADVERTENCIA DE SEGURIDAD

**NUNCA** subas archivos con valores reales a repositorios públicos. Estos archivos contienen:
- Cookies de sesión
- Tokens de autenticación
- IDs de usuario

Siempre usa archivos `.example` en repositorios públicos.

## Estructura de Valores a Reemplazar

- `YOUR_TIMEZONE` - Tu zona horaria (ej: Atlantic.Canary)
- `YOUR_SOCS_COOKIE_VALUE` - Cookie SOCS
- `YOUR_SSID_VALUE` - Cookie SSID
- `YOUR_SAPISID_COOKIE_VALUE` - Cookie SAPISID
- `YOUR_SECURE_*PSID*` - Cookies PSID cifradas
- `YOUR_LOGIN_INFO_VALUE` - Info de login codificada
- `YOUR_TIMESTAMP_YOUR_HASH_VALUE` - Token de autorización SAPISID
- Otros valores según corresponda

## Licencia

Estos archivos de ejemplo están disponibles bajo la misma licencia que el proyecto.
