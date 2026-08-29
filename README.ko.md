# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box는 라이브 방송을 자동 모니터링하고 녹화하는 Windows x64용 로컬 앱입니다. 카드 UI, 일괄 제어, 분할 녹화, MP4 리먹싱, 기록, 로그, 시스템 트레이, 이전 설정 가져오기를 제공합니다. 현재 버전은 `0.2.0`입니다. 계정이 필요 없고 Cookie를 저장하지 않습니다.

## 다운로드 및 설치

Releases에서 `RecoBox-Setup-0.2.0.exe`와 `.sha256.txt`를 받으세요. 설치 프로그램은 서명되지 않았습니다. LiveMe용으로 검증된 최소 Node.js v24.20.0 LTS 런타임이 포함됩니다.

## 플랫폼

기존: Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube, JD. Taobao는 고정된 리졸버가 로그인 세션을 요구하므로 비활성화되어 있습니다.

신규 Beta: Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto, Shopee Live. 출시 전 공개 샘플로 방송 중/오프라인 상태, 스트림 URL, 짧은 녹화를 검증해야 합니다. 제한된 방은 익명 접근 불가 오류를 반환하며 로그인을 시도하지 않습니다. Kick, Facebook Live, Instagram Live는 범위에서 제외됩니다.

## 녹화, 프록시 및 언어

- 분할은 기본적으로 꺼져 있습니다. 활성화하면 1, 2, 3…으로 번호가 붙고 마지막 조각은 실제 길이를 유지합니다.
- 경로: `스트리머 / 날짜 / 시작 시간 / 동영상`; TS는 재인코딩 없이 MP4로 리먹싱할 수 있습니다.
- 전역 프록시는 새 방만 상속하며 방별로 덮어쓸 수 있습니다. 인증 정보 없는 HTTP/HTTPS만 허용하고 리졸버와 FFmpeg 모두에 적용하며 로그에는 기록하지 않습니다.
- 10개 언어는 재시작 없이 즉시 전환됩니다. 새 설치는 지원되는 Windows 언어를 따르고, 이전 DB는 중국어 간체를 유지하며, 사용자의 선택은 저장됩니다.

## 개인정보 및 보안

DB, 로그, 설정은 로컬에 남습니다. 일부 상류 리졸버 요청은 TLS 인증서 검증을 끄므로 신뢰할 수 있는 네트워크에서 사용하세요. [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)를 참조하세요.

## 소스 실행 및 빌드

Windows x64, Python 3.12, PowerShell 7이 필요합니다. `.[dev]`를 설치하고 `runtime/ffmpeg`를 준비하며 LiveMe용 `tools/prepare_node.ps1`를 실행하세요. `pytest tests -q`, `packaging/build.ps1`, `packaging/build_installer.ps1` 순서로 실행합니다. 바이너리는 Git에 커밋하지 않습니다.

## Roadmap

- 호환 가능한 곳에서 TLS 검증 복원
- Xiaohongshu, TikTok 및 해외 Beta 안정화
- 자동 업데이트와 연결 중단 복구
- 익명 공개 플랫폼 추가
- Windows 서명, 패키징, CI 개선

## 기여, 라이선스 및 면책

[CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요. 자체 코드는 [MIT License](LICENSE)를 사용합니다. 저장 권한이 있는 콘텐츠만 녹화하고 플랫폼 약관, 저작권, 개인정보 및 현지 법률을 준수하세요.
