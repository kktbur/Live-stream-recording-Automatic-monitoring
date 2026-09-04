# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box 是 Windows x64 的本機直播自動監控與錄製工具，提供卡片式介面、批次控制、分段錄製、MP4 封裝、歷史、日誌、系統匣與舊設定匯入。目前版本為 `0.2.1`。不需要 Reco Box 或直播平台帳號，不保存 Cookie。

## 下載與安裝

從 Releases 下載 `RecoBox-Setup-0.2.1.exe` 與對應的 `.sha256.txt`。安裝包未簽署，SmartScreen 可能顯示未知發行者。安裝包內含已校驗的 Node.js v24.20.0 LTS 最小執行環境，使用者不必另行安裝。

## 平台

原有平台：抖音、快手、Bilibili、小紅書、TikTok、YouTube、京東；淘寶因鎖定解析器需要登入而暫不啟用。

新增 Beta：Twitch、SOOP Global、CHZZK、TwitCasting、SHOWROOM、BIGO LIVE、17LIVE、LiveMe、Picarto、Shopee Live。Beta 代表已完成程式適配，但仍需以公開直播做上線、離線、串流位址及短時錄製驗證。受限內容會回報匿名存取不可用，不會嘗試登入。專案不加入 Kick、Facebook Live 或 Instagram Live。

## 錄製、代理與語言

- 預設不分段；輸入分鐘數後依 1、2、3…命名，最後一段保留實際長度。
- 目錄為 `主播名稱 / 年月日 / 場次開始時間 / 影片`；可在完成後將 TS 無損封裝為 MP4。
- 全域代理只供新直播間繼承；每個直播間可覆寫。只接受不含帳密的 HTTP/HTTPS 代理，並同時傳給解析器與 FFmpeg，不寫入日誌。
- 設定中可立即切換十種語言，無需重啟。新安裝跟隨支援的 Windows 語言；舊資料庫預設簡體中文；手動選擇會永久保存。

## 隱私與安全

資料庫、日誌與設定保存在本機。錄製內容只寫入使用者指定目錄。上游解析器的部分請求停用 TLS 憑證驗證，可能受中間人攻擊；請在可信網路使用。詳見 [PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md) 與 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 從原始碼執行與建置

需要 Windows x64、Python 3.12、PowerShell 7。先安裝 `.[dev]`，準備 `runtime/ffmpeg`，LiveMe 另執行 `pwsh -NoProfile -File tools/prepare_node.ps1`。測試使用 `pytest tests -q`；建置依序執行 `packaging/build.ps1` 與 `packaging/build_installer.ps1`。FFmpeg 與 Node.js 二進位不提交 Git。

## Roadmap

- 在相容平台恢復 TLS 驗證
- 改善小紅書、TikTok 與海外 Beta 穩定性
- 加入自動更新檢查
- 改善斷線後的錄製恢復
- 增加匿名公開平台
- 改善 Windows 簽署、打包與 CI

## 貢獻、授權與免責

Issue、PR、平台失效與新平台適配流程見 [CONTRIBUTING.md](CONTRIBUTING.md)。自有程式碼採 [MIT License](LICENSE)。只應錄製你有權保存的內容；使用者須遵守平台條款、著作權、隱私及所在地法律。
