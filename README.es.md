# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box es una aplicación local para Windows x64 que supervisa y graba directos automáticamente. Incluye interfaz de tarjetas, controles por lotes, segmentos, conversión sin recodificar a MP4, historial, registros, bandeja del sistema e importación de configuraciones antiguas. Versión actual: `0.2.1`. No requiere cuentas ni guarda cookies.

## Descarga e instalación

Descargue `RecoBox-Setup-0.2.1.exe` y su archivo `.sha256.txt` desde Releases. El instalador no está firmado. Incluye un entorno mínimo y verificado de Node.js v24.20.0 LTS para LiveMe.

## Plataformas

Plataformas existentes: Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube y JD. Taobao sigue desactivado porque el analizador fijado exige una sesión iniciada.

Nuevas Beta: Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto y Shopee Live. Beta exige validar estados en directo/sin directo, URL del flujo y una grabación corta antes de publicar. El contenido restringido devuelve “acceso anónimo no disponible”; nunca se inicia sesión. Kick, Facebook Live e Instagram Live quedan fuera.

## Grabación, proxy e idiomas

- La segmentación está desactivada por defecto; los segmentos se numeran 1, 2, 3… y el último conserva su duración real.
- Ruta: `streamer / fecha / hora de inicio / vídeo`; TS puede convertirse a MP4 sin recodificar.
- El proxy global solo lo heredan las salas nuevas; cada sala puede reemplazarlo. Solo HTTP/HTTPS sin credenciales; se aplica al analizador y a FFmpeg y no se registra.
- Los diez idiomas cambian al instante. Una instalación nueva sigue el idioma compatible de Windows; una base antigua usa chino simplificado; la elección queda guardada.

## Privacidad y seguridad

Base de datos, registros y ajustes permanecen localmente. Algunas peticiones del analizador superior desactivan la verificación TLS; use una red fiable. Consulte [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md) y [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Código fuente y compilación

Requiere Windows x64, Python 3.12 y PowerShell 7. Instale `.[dev]`, prepare `runtime/ffmpeg` y ejecute `tools/prepare_node.ps1` para LiveMe. Ejecute `pytest tests -q`, `packaging/build.ps1` y `packaging/build_installer.ps1`. Los binarios no se guardan en Git.

## Roadmap

- Recuperar TLS donde sea compatible
- Mejorar Xiaohongshu, TikTok y las Beta internacionales
- Añadir actualización automática y recuperación tras cortes
- Añadir plataformas públicas anónimas
- Mejorar firma, empaquetado y CI de Windows

## Contribución, licencia y aviso

Consulte [CONTRIBUTING.md](CONTRIBUTING.md). El código propio usa [MIT License](LICENSE). Grabe solo contenido autorizado y respete términos, derechos de autor, privacidad y leyes locales.
