# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box は、ライブ配信を自動監視・録画する Windows x64 向けローカルアプリです。カード UI、一括操作、分割録画、MP4 リマックス、履歴、ログ、システムトレイ、旧設定のインポートを備えます。現在のバージョンは `0.2.0` です。アカウントは不要で、Cookie は保存しません。

## ダウンロードとインストール

Releases から `RecoBox-Setup-0.2.0.exe` と `.sha256.txt` を取得してください。インストーラーは未署名です。LiveMe 用に検証済みの最小 Node.js v24.20.0 LTS ランタイムを同梱します。

## 対応プラットフォーム

既存：Douyin、Kuaishou、Bilibili、Xiaohongshu、TikTok、YouTube、JD。Taobao は固定リゾルバーがログインを要求するため無効です。

新規 Beta：Twitch、SOOP Global、CHZZK、TwitCasting、SHOWROOM、BIGO LIVE、17LIVE、LiveMe、Picarto、Shopee Live。公開前に、公開サンプルで配信中・停止中、ストリーム URL、短時間録画を検証します。制限付きルームは匿名アクセス不可を返し、ログインは試みません。Kick、Facebook Live、Instagram Live は対象外です。

## 録画、プロキシ、言語

- 分割は既定で無効です。有効時は 1、2、3…で採番し、最後は実際の長さになります。
- 保存先は `配信者 / 日付 / 開始時刻 / 動画`。TS は再エンコードせず MP4 にできます。
- グローバルプロキシは新規ルームだけが継承し、ルームごとに上書き可能です。認証情報なしの HTTP/HTTPS のみをリゾルバーと FFmpeg に渡し、ログには残しません。
- 10 言語は再起動なしで即時切替できます。新規は対応 Windows 言語、旧 DB は簡体字中国語、手動選択は保存されます。

## プライバシーとセキュリティ

DB、ログ、設定はローカルに保持します。上流リゾルバーの一部通信は TLS 証明書検証を無効化しているため、信頼できるネットワークで使用してください。[PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。

## ソースから実行・ビルド

Windows x64、Python 3.12、PowerShell 7 が必要です。`.[dev]` と `runtime/ffmpeg` を用意し、LiveMe 用に `tools/prepare_node.ps1` を実行します。`pytest tests -q`、`packaging/build.ps1`、`packaging/build_installer.ps1` の順に実行します。バイナリは Git に含めません。

## Roadmap

- 互換可能な通信で TLS 検証を復元
- Xiaohongshu、TikTok、海外 Beta の安定化
- 自動更新と切断後の復旧
- 匿名公開プラットフォームの追加
- Windows 署名、パッケージ、CI の改善

## 貢献、ライセンス、免責

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。独自コードは [MIT License](LICENSE) です。保存する権利のある内容だけを録画し、規約、著作権、プライバシー、地域法を守ってください。
