# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box 是一款面向 Windows 的本地直播自动监控与录制软件。它提供卡片式桌面界面、批量监控、直播开播自动录制、手动立即检查、分段录制、录制完成转 MP4、历史记录、运行日志、系统托盘和旧配置一键导入。

软件无需 Reco Box 账号，也不会把直播间列表、录制记录或视频上传到 Reco Box 服务器。平台解析采用匿名模式，不导入账号 Cookie。

> 当前为 `0.2.1` 早期测试版，仅面向 Windows x64。直播平台经常调整网页和接口，因此“已支持”不代表任何直播间都能永久稳定解析。

## 下载与安装

在仓库右侧的 **Releases** 页面下载：

- `RecoBox-Setup-0.2.1.exe`：Windows 标准安装包
- `RecoBox-Setup-0.2.1.exe.sha256.txt`：安装包校验值

安装前建议核对 SHA-256。安装包目前没有商业代码签名，Windows SmartScreen 可能显示“未知发布者”。

安装完成后直接打开 Reco Box 即可。安装包已内置经过 SHA-256 校验的 Node.js v24.20.0 LTS 最小运行时，专供 LiveMe 的 JavaScript 签名流程使用，不要求用户另行安装 Node.js。

## 主要平台

| 平台 | 当前状态 | 说明 |
| --- | --- | --- |
| 抖音 | 支持 | 匿名解析与自动监控 |
| 快手 | 支持 | 匿名解析与自动监控 |
| Bilibili | 支持 | 匿名解析与自动监控；API 请求已接入第一方 TLS 默认校验 |
| 小红书 | 支持 | 匿名解析；稳定性受平台变化影响 |
| TikTok | 支持 | 匿名解析；部分地区可能需要可用网络环境 |
| YouTube | 支持 | 匿名解析；直播源可用性取决于房间状态 |
| 京东 | 支持 | 匿名解析；稳定性受平台变化影响 |
| 淘宝 | 暂不启用 | 锁定版解析器需要登录会话，本项目不会绕过登录或导入 Cookie |
| Twitch | Beta | 公开直播匿名解析 |
| SOOP Global | Beta | 仅公开、匿名可访问内容；受限内容不会尝试登录 |
| CHZZK | Beta | 公开直播匿名解析 |
| TwitCasting | Beta | 仅公开房间；登录保护内容明确拒绝 |
| SHOWROOM | Beta | 公开直播匿名解析 |
| BIGO LIVE | Beta | 公开直播匿名解析 |
| 17LIVE | Beta | 公开直播匿名解析 |
| LiveMe | Beta | 使用安装包内置 Node.js 签名运行时 |
| Picarto | Beta | 公开直播匿名解析 |
| Shopee Live | Beta | 覆盖已识别的区域站点公开直播 |

“Beta”表示代码适配已经加入，但平台接口可能变化；发布前必须通过公开样本的开播、未开播、流地址和短时录制验证。Reco Box 不加入 Kick、Facebook Live、Instagram Live，不保存 Cookie，也不绕过付费、年龄、地区、私密或登录访问控制。

## 录制规则

- 默认不分段；启用后可输入分钟数，例如输入 `5` 即每 5 分钟生成一段，最后不足 5 分钟的片段按实际时长保存。
- 分段文件按 `1`、`2`、`3`……编号。
- 输出目录结构为：`主播名字 / 年月日 / 场次开始时间（24 小时制） / 视频文件`。
- 可选择 TS 输出，并在录制完成后无损封装为 MP4；成功后可删除对应 TS。
- 手动停止会暂停该直播间的监控，不会在五秒重试后自动重新开始。
- 可设置全局默认代理，新直播间会继承；每个直播间可以单独覆盖。只接受不含账号密码的 HTTP/HTTPS 代理，代理同时用于平台解析和 FFmpeg，不写入运行日志。

## 界面语言

设置页可即时切换简体中文、繁體中文、English、Español、Français、Deutsch、Português、Русский、日本語和한국어，无需重启。新安装首次启动跟随受支持的 Windows 语言，无法识别时使用简体中文；旧数据库升级后保持简体中文，手动选择会永久保存。

## 隐私与本地数据

数据库、运行日志、导入报告和上游运行文件保存在当前 Windows 用户的应用数据目录；录制视频只写入用户指定的文件夹。详细说明见 [PRIVACY.md](PRIVACY.md)。

旧配置导入只读取直播间地址及非敏感录制偏好，不导入或展示 Cookie、账号令牌、通知密钥和代理凭据。

## 从源码运行

要求：Windows x64、Python 3.12、PowerShell 7。开发版若需 LiveMe，请运行 `tools/prepare_node.ps1` 下载并校验固定 Node.js 运行时。

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -e ".[dev]"
./.venv/Scripts/reco-box.exe
```

运行测试：

完整测试会真实调用 FFmpeg。请先按下方构建说明，把经过校验的 FFmpeg 运行时放入 `runtime/ffmpeg/`；二进制缺失时，预览解码和核心自检测试会失败。

```powershell
$env:QT_QPA_PLATFORM='offscreen'
./.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
```

## 构建 Windows 安装包

源码仓库不提交 FFmpeg 或 Node.js 二进制。发布者需要准备经过校验的 FFmpeg 运行时，并运行 `tools/prepare_node.ps1`；许可证文本保留在对应 runtime 目录，来源与校验值记录在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

安装 Inno Setup 后运行：

```powershell
pwsh -NoProfile -File ./packaging/build.ps1
pwsh -NoProfile -File ./packaging/build_installer.ps1
```

打包后的程序支持离线自检：

```powershell
& "./dist/Reco Box/RecoBox.exe" --self-test
```

## 项目结构

- `src/reco_box/`：应用、录制、监控、存储和桌面 UI
- `vendor/DouyinLiveRecorder/`：锁定的上游解析源码与许可证
- `tests/`：核心行为与 UI 冒烟测试
- `packaging/`：PyInstaller 与 Inno Setup 构建配置
- `runtime/ffmpeg/`：本地发布构建输入；二进制不进入 Git 历史

参与开发、报告平台失效或提交新平台适配前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按 [SECURITY.md](SECURITY.md) 私密报告。

## Roadmap

- Improve TLS verification compatibility.
- Improve Xiaohongshu, TikTok, and overseas Beta resolver stability.
- Add automatic update checking.
- Improve recording recovery after network interruption.
- Add additional livestream platforms within the anonymous-access boundary.
- Improve Windows packaging and code signing.
- Expand GitHub Actions CI and Windows regression coverage.

Roadmap 表示当前方向，不构成发布时间或平台长期可用性的承诺。具体工作通过 GitHub Issues 跟踪。

## 许可证与免责声明

Reco Box 自有代码采用 [MIT License](LICENSE)。上游解析器、FFmpeg、Qt/PySide6 和其他依赖保留各自许可证，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本软件仅用于录制你有权保存的内容。使用者应自行遵守直播平台条款、著作权、隐私权及所在地法律。项目不保证平台接口长期可用，也不提供绕过登录、访问控制或付费限制的功能。

## 网络安全说明

锁定的上游直播解析器对多数主要平台解析请求仍默认不校验 TLS 证书。这是上游为兼容部分反爬环境保留的设计，可能降低网络传输的抗中间人攻击能力；请仅在可信网络环境中使用。PR-06 已建立 [平台网络安全矩阵](docs/platform-network-security.md)，并将 Reco Box 自己控制的 TwitCasting 匿名请求接入默认校验 TLS 的第一方策略；PR-07 又将 Bilibili API 请求迁移到第一方 HTTPX 客户端并默认校验证书。其他上游路径仍需逐平台验证，不能把这两步理解为所有平台已经完成整改。Reco Box 当前不会把解析到的临时直播地址写入日志。

## 版本 0.2.1

- 统一项目版本、Python 包、PyInstaller、Inno Setup 安装器和十语言 README 的发布标识。
- 在 Windows CI 中覆盖旧版安装器到新版覆盖安装、安装后 self-check、静默卸载和用户数据保留。
- 为正式 Tag/手动发布流程加入 SHA-256 校验与 GitHub Artifact Attestation；普通 CI 不发布公开 Release。

## 版本 0.2.0

- 新增十语言界面、托盘菜单、安装器和完整 README，并支持设置内即时切换。
- 新增十个匿名海外 Beta 平台适配、全局/直播间代理和 LiveMe 内置 Node.js 运行时。
- 保留原有卡片界面、目录结构、分段编号、MP4 封装和旧数据库数据。

## 版本 0.1.4

- 发布前隐私与凭据审计，隔离本地数据库、日志、配置和构建产物。
- 项目改为独立源码结构，构建时不再依赖仓库外部路径。
- 公共安装包改用 SHA-256 校验的 FFmpeg 9.0.1 LGPL shared 构建。
- 保留 0.1.2 的卡片式主界面、筛选排序搜索、批量控制、可滚动编辑页、分段与 MP4 封装、实时大小修正和 Qt Multimedia 预览修复。
- 关闭 UPX 压缩，降低未签名 Windows 构建的杀毒软件误报概率。
- Node.js 缺失改为可选自检项，不再阻断当前核心平台使用。
- 补充 TLS 证书校验风险披露与上游 v4.0.7 逐文件核对记录。
