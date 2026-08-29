# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box ist eine lokale Windows-x64-Anwendung zur automatischen Überwachung und Aufzeichnung von Livestreams. Sie bietet Kartenansicht, Sammelsteuerung, Segmentierung, MP4-Remuxing, Verlauf, Protokolle, Infobereich und Import alter Konfigurationen. Aktuelle Version: `0.2.0`. Konten sind nicht nötig; Cookies werden nicht gespeichert.

## Download und Installation

`RecoBox-Setup-0.2.0.exe` und die zugehörige `.sha256.txt` unter Releases herunterladen. Das Installationspaket ist nicht signiert. Für LiveMe enthält es eine geprüfte minimale Node.js-v24.20.0-LTS-Laufzeit.

## Plattformen

Bestehend: Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube und JD. Taobao bleibt deaktiviert, weil der fixierte Resolver eine angemeldete Sitzung verlangt.

Neue Beta-Plattformen: Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto und Shopee Live. Vor einer Veröffentlichung müssen Live-/Offline-Status, Stream-URL und eine kurze Aufnahme mit öffentlichen Beispielen geprüft werden. Geschützte Inhalte melden „anonymer Zugriff nicht verfügbar“; eine Anmeldung wird nie versucht. Kick, Facebook Live und Instagram Live sind ausgeschlossen.

## Aufnahme, Proxy und Sprachen

- Segmentierung ist standardmäßig aus; Dateien heißen 1, 2, 3… und das letzte Segment behält seine tatsächliche Dauer.
- Ablage: `Streamer / Datum / Startzeit / Video`; TS kann verlustfrei nach MP4 umgepackt werden.
- Der globale Proxy gilt nur für neue Räume; jeder Raum kann ihn überschreiben. Nur HTTP/HTTPS ohne Zugangsdaten; Resolver und FFmpeg nutzen denselben Proxy, Protokolle enthalten ihn nicht.
- Alle zehn Sprachen wechseln sofort. Neuinstallationen folgen einer unterstützten Windows-Sprache; alte Datenbanken bleiben auf vereinfachtem Chinesisch; die Auswahl wird gespeichert.

## Datenschutz und Sicherheit

Datenbank, Protokolle und Einstellungen bleiben lokal. Einige Upstream-Anfragen deaktivieren die TLS-Zertifikatsprüfung; nur in vertrauenswürdigen Netzen verwenden. Siehe [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md) und [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Quellcode und Build

Benötigt Windows x64, Python 3.12 und PowerShell 7. `.[dev]` installieren, `runtime/ffmpeg` vorbereiten und für LiveMe `tools/prepare_node.ps1` ausführen. Danach `pytest tests -q`, `packaging/build.ps1` und `packaging/build_installer.ps1`. Binärdateien werden nicht in Git gespeichert.

## Roadmap

- TLS-Prüfung soweit kompatibel wiederherstellen
- Xiaohongshu, TikTok und internationale Betas stabilisieren
- Automatische Updates und Wiederaufnahme nach Abbrüchen
- Weitere anonym zugängliche Plattformen
- Windows-Signierung, Packaging und CI verbessern

## Mitwirken, Lizenz und Haftung

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Eigener Code steht unter der [MIT License](LICENSE). Nur berechtigte Inhalte aufnehmen und Plattformregeln, Urheberrecht, Datenschutz und lokales Recht beachten.
