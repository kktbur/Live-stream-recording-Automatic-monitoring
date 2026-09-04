# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box é uma aplicação local para Windows x64 que monitoriza e grava transmissões ao vivo automaticamente. Inclui interface em cartões, controlos em lote, segmentação, remux para MP4, histórico, registos, área de notificação e importação de configurações antigas. Versão atual: `0.2.1`. Não requer contas e não guarda cookies.

## Download e instalação

Transfira `RecoBox-Setup-0.2.1.exe` e o ficheiro `.sha256.txt` em Releases. O instalador não tem assinatura digital. Inclui um runtime mínimo e verificado do Node.js v24.20.0 LTS para LiveMe.

## Plataformas

Existentes: Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube e JD. Taobao continua desativado porque o resolvedor fixado exige uma sessão autenticada.

Novas Beta: Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto e Shopee Live. Antes do lançamento, uma Beta deve validar estados online/offline, URL do fluxo e uma gravação curta com amostras públicas. Conteúdo restrito devolve “acesso anónimo indisponível” sem tentar iniciar sessão. Kick, Facebook Live e Instagram Live ficam fora do âmbito.

## Gravação, proxy e idiomas

- A segmentação vem desligada; os ficheiros são 1, 2, 3… e o último mantém a duração real.
- Estrutura: `streamer / data / hora inicial / vídeo`; TS pode ser remuxado para MP4.
- O proxy global só é herdado por novas salas; cada sala pode substituí-lo. Apenas HTTP/HTTPS sem credenciais; aplica-se ao resolvedor e FFmpeg e não aparece nos registos.
- Os dez idiomas mudam imediatamente. Novas instalações seguem um idioma Windows suportado; bases antigas ficam em chinês simplificado; a escolha é guardada.

## Privacidade e segurança

Base de dados, registos e definições permanecem locais. Alguns pedidos do resolvedor a montante desativam a verificação TLS; use uma rede de confiança. Consulte [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md) e [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Código-fonte e compilação

Requer Windows x64, Python 3.12 e PowerShell 7. Instale `.[dev]`, prepare `runtime/ffmpeg` e execute `tools/prepare_node.ps1` para LiveMe. Execute `pytest tests -q`, `packaging/build.ps1` e `packaging/build_installer.ps1`. Os binários não são enviados para Git.

## Roadmap

- Restaurar TLS quando compatível
- Melhorar Xiaohongshu, TikTok e Betas internacionais
- Adicionar atualização automática e recuperação de interrupções
- Adicionar plataformas públicas anónimas
- Melhorar assinatura, pacote e CI do Windows

## Contribuição, licença e aviso

Consulte [CONTRIBUTING.md](CONTRIBUTING.md). O código próprio usa a [MIT License](LICENSE). Grave apenas conteúdo autorizado e cumpra termos, direitos de autor, privacidade e legislação local.
