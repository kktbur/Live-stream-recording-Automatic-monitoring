# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box est une application locale Windows x64 de surveillance et d’enregistrement automatiques des directs. Elle offre une interface en cartes, des commandes groupées, le découpage, le remuxage MP4, l’historique, les journaux, la zone de notification et l’import d’anciennes configurations. Version actuelle : `0.2.1`. Aucun compte n’est requis et aucun cookie n’est conservé.

## Téléchargement et installation

Téléchargez `RecoBox-Setup-0.2.1.exe` et son fichier `.sha256.txt` depuis Releases. L’installeur n’est pas signé. Il intègre un environnement minimal Node.js v24.20.0 LTS vérifié pour LiveMe.

## Plateformes

Plateformes existantes : Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube et JD. Taobao reste désactivé car le résolveur verrouillé exige une session connectée.

Nouvelles Beta : Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto et Shopee Live. Une Beta doit valider les états en ligne/hors ligne, l’URL du flux et un court enregistrement avant publication. Les contenus restreints renvoient une erreur d’accès anonyme sans tentative de connexion. Kick, Facebook Live et Instagram Live sont exclus.

## Enregistrement, proxy et langues

- Le découpage est désactivé par défaut ; les fichiers sont numérotés 1, 2, 3… et le dernier garde sa durée réelle.
- Arborescence : `streamer / date / heure de début / vidéo` ; TS peut être remuxé en MP4.
- Le proxy global n’est hérité que par les nouvelles salles ; chaque salle peut le remplacer. Seuls HTTP/HTTPS sans identifiants sont acceptés, pour le résolveur et FFmpeg, sans écriture dans les journaux.
- Les dix langues changent immédiatement. Une nouvelle installation suit une langue Windows prise en charge ; une ancienne base reste en chinois simplifié ; le choix est mémorisé.

## Confidentialité et sécurité

Base, journaux et réglages restent locaux. Certaines requêtes du résolveur amont désactivent la vérification TLS ; utilisez un réseau fiable. Voir [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md) et [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Source et compilation

Nécessite Windows x64, Python 3.12 et PowerShell 7. Installez `.[dev]`, préparez `runtime/ffmpeg`, puis lancez `tools/prepare_node.ps1` pour LiveMe. Exécutez `pytest tests -q`, `packaging/build.ps1` et `packaging/build_installer.ps1`. Les binaires ne sont pas commités.

## Roadmap

- Rétablir TLS quand c’est compatible
- Stabiliser Xiaohongshu, TikTok et les Beta internationales
- Ajouter mise à jour automatique et reprise après coupure
- Ajouter des plateformes publiques anonymes
- Améliorer signature, packaging et CI Windows

## Contribution, licence et avertissement

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Le code propre est sous [MIT License](LICENSE). N’enregistrez que les contenus autorisés et respectez conditions, droits d’auteur, vie privée et lois locales.
