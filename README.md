# Reco Box

Reco Box 是一款面向 Windows 的本地直播自动监控与录制软件。它提供卡片式桌面界面、批量监控、直播开播自动录制、手动立即检查、分段录制、录制完成转 MP4、历史记录、运行日志、系统托盘和旧配置一键导入。

软件无需 Reco Box 账号，也不会把直播间列表、录制记录或视频上传到 Reco Box 服务器。平台解析采用匿名模式，不导入账号 Cookie。

> 当前为 `0.1.4` 早期测试版，仅面向 Windows x64。直播平台经常调整网页和接口，因此“已支持”不代表任何直播间都能永久稳定解析。

## 下载与安装

在仓库右侧的 **Releases** 页面下载：

- `RecoBox-Setup-0.1.4.exe`：Windows 标准安装包
- `RecoBox-Setup-0.1.4.exe.sha256.txt`：安装包校验值

安装前建议核对 SHA-256。安装包目前没有商业代码签名，Windows SmartScreen 可能显示“未知发布者”。

安装完成后直接打开 Reco Box 即可。Node.js 是部分上游平台 JavaScript 签名流程的可选依赖，不是当前已公开平台的必需组件；如果以后启用相关平台，自检会提示是否需要安装 Node.js 18 或更高版本。

## 主要平台

| 平台 | 当前状态 | 说明 |
| --- | --- | --- |
| 抖音 | 支持 | 匿名解析与自动监控 |
| 快手 | 支持 | 匿名解析与自动监控 |
| Bilibili | 支持 | 匿名解析与自动监控 |
| 小红书 | 支持 | 匿名解析；稳定性受平台变化影响 |
| TikTok | 支持 | 匿名解析；部分地区可能需要可用网络环境 |
| YouTube | 支持 | 匿名解析；直播源可用性取决于房间状态 |
| 京东 | 支持 | 匿名解析；稳定性受平台变化影响 |
| 淘宝 | 暂不启用 | 锁定版解析器需要登录会话，本项目不会绕过登录或导入 Cookie |

## 录制规则

- 默认不分段；启用后可输入分钟数，例如输入 `5` 即每 5 分钟生成一段，最后不足 5 分钟的片段按实际时长保存。
- 分段文件按 `1`、`2`、`3`……编号。
- 输出目录结构为：`主播名字 / 年月日 / 场次开始时间（24 小时制） / 视频文件`。
- 可选择 TS 输出，并在录制完成后无损封装为 MP4；成功后可删除对应 TS。
- 手动停止会暂停该直播间的监控，不会在五秒重试后自动重新开始。

## 隐私与本地数据

数据库、运行日志、导入报告和上游运行文件保存在当前 Windows 用户的应用数据目录；录制视频只写入用户指定的文件夹。详细说明见 [PRIVACY.md](PRIVACY.md)。

旧配置导入只读取直播间地址及非敏感录制偏好，不导入或展示 Cookie、账号令牌、通知密钥和代理凭据。

## 从源码运行

要求：Windows x64、Python 3.12、PowerShell 7。Node.js 18+ 仅在启用依赖 JavaScript 签名的上游平台时需要。

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -e ".[dev]"
./.venv/Scripts/reco-box.exe
```

运行测试：

```powershell
$env:QT_QPA_PLATFORM='offscreen'
./.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
```

## 构建 Windows 安装包

源码仓库不提交 FFmpeg 二进制。发布者需要把 FFmpeg Windows x64 LGPL shared 版本中的 `ffmpeg.exe`、`ffprobe.exe`、所需 DLL 与 `LICENSE.txt` 放入 `runtime/ffmpeg/`，并更新 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 中的准确版本、提交、校验值和源码链接。

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

## 许可证与免责声明

Reco Box 自有代码采用 [MIT License](LICENSE)。上游解析器、FFmpeg、Qt/PySide6 和其他依赖保留各自许可证，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本软件仅用于录制你有权保存的内容。使用者应自行遵守直播平台条款、著作权、隐私权及所在地法律。项目不保证平台接口长期可用，也不提供绕过登录、访问控制或付费限制的功能。

## 网络安全说明

当前锁定的上游直播解析器对主要平台解析请求默认不校验 TLS 证书。这是上游为兼容部分反爬环境保留的设计，可能降低网络传输的抗中间人攻击能力；请仅在可信网络环境中使用。Reco Box 当前不会把解析到的临时直播地址写入日志。后续版本会逐个平台测试并逐步恢复证书校验，必要时只为特定请求保留兼容例外。

## 版本 0.1.4

- 发布前隐私与凭据审计，隔离本地数据库、日志、配置和构建产物。
- 项目改为独立源码结构，构建时不再依赖仓库外部路径。
- 公共安装包改用 SHA-256 校验的 FFmpeg 9.0.1 LGPL shared 构建。
- 保留 0.1.2 的卡片式主界面、筛选排序搜索、批量控制、可滚动编辑页、分段与 MP4 封装、实时大小修正和 Qt Multimedia 预览修复。
- 关闭 UPX 压缩，降低未签名 Windows 构建的杀毒软件误报概率。
- Node.js 缺失改为可选自检项，不再阻断当前核心平台使用。
- 补充 TLS 证书校验风险披露与上游 v4.0.7 逐文件核对记录。
