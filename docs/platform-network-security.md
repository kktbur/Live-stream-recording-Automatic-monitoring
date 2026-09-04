# Platform Network Security Matrix

调查日期：2026-09-04（Asia/Shanghai）

## 调查边界

本表是 PR-06 第一阶段的静态网络路径盘点。它根据 Reco Box 当前暴露的
`Platform` 枚举、第一方 Resolver 调用和锁定的 DouyinLiveRecorder v4.0.7 源码整理，
不使用账号、Cookie、密码或通知密钥，也不把临时播放地址写入仓库。

本轮的“未迁移”不是“平台证书一定无效”，而是该请求仍沿用上游
`async_req(..., verify=False)` 默认值，尚未完成 Reco Box 自己的逐平台兼容验证。
动态返回的 CDN 播放地址也需要在后续公开样本测试中单独记录。

## 状态定义

| 状态 | 含义 |
| --- | --- |
| 第一方已验证 | Reco Box 自己控制的请求明确传入 `verify=True`；本 PR 只覆盖 TwitCasting 匿名路径。 |
| 上游默认未迁移 | 请求经锁定上游的 `async_req`，当前默认 `verify=False`；不能宣称已恢复 TLS 校验。 |
| 直接客户端默认校验 | 上游直接创建 `httpx.AsyncClient` 且未覆盖 `verify`，按 HTTPX 默认行为校验；仍需平台公开样本验证。 |
| 明文 HTTP | URL 本身是 `http://`，没有 TLS 证书可校验；后续需单独决定是否能移除或替换。 |
| 不调用 | Reco Box 因匿名访问边界不会调用该登录接口。 |

## 当前暴露平台

| 平台 | 主要请求 Endpoint/Host | 当前请求路径 | TLS 状态 | 匿名访问边界与下一步 |
| --- | --- | --- | --- | --- |
| 抖音 | `live.douyin.com`、`webcast.amemv.com`、`www.iesdouyin.com` | 上游 `async_req`；少数重定向辅助请求为直接 HTTPX | 上游默认未迁移；辅助请求为直接客户端默认校验 | 仅匿名解析；下一步分别验证页面、API 和动态播放地址 |
| 快手 | `live.kuaishou.com`、`livev.m.chenzhongtech.com` | 上游 `async_req` | 上游默认未迁移 | 仅公开匿名页面；需要公开样本复核 |
| Bilibili | `api.live.bilibili.com` | 上游 `async_req` | 上游默认未迁移 | 公开匿名解析；需要验证 API 与播放地址 |
| 小红书 | `www.xiaohongshu.com`、`app.xhs.cn`；媒体可能为 `live-source-play.xhscdn.com` | 上游 `async_req` | 上游默认未迁移；部分媒体地址可能为明文 HTTP | 仅匿名解析；后续单独处理明文媒体地址 |
| TikTok | 输入页面 `www.tiktok.com` / `tiktok.com`；播放 Host 从 `LiveRoom.liveRoom.streamData` 动态返回 | 页面请求经上游 `async_req`；播放地址由上游 `stream.py` 解析 | 上游默认未迁移 | 需要可用地区网络；不登录、不导入 Cookie；动态 CDN Host 需公开样本复核 |
| YouTube | 输入页面 `youtube.com` / `youtu.be`；播放 Host 从 `streamingData.hlsManifestUrl` 动态返回 | 页面请求和 HLS 清单请求经上游 `async_req` | 上游默认未迁移 | 仅公开匿名直播；不把动态 CDN Host 固化为静态例外，需公开样本复核 |
| 京东 | `lives.jd.com`、`api.m.jd.com` | 上游 `async_req` | 上游默认未迁移 | 公开匿名解析；需要验证重定向、API 和播放地址 |
| 淘宝 | `h5api.m.taobao.com` | Reco Box 在 Resolver 中拒绝调用 | 不调用 | 锁定解析器要求登录会话；不绕过登录或导入 Cookie |
| Twitch | `gql.twitch.tv`、`usher.ttvnw.net` | 上游 `async_req`；播放地址动态返回 | 上游默认未迁移 | 仅公开频道；需重新选择公开直播样本验证 |
| SOOP Global | 输入页面 `www.sooplive.com`；`api.sooplive.com`；`global-media.sooplive.com` | `.com` 路径由上游 `async_req` 请求频道/流信息和 HLS 清单 | 上游默认未迁移 | 仅公开匿名内容；锁定上游另含未被 Reco Box `.com` 路径选中的旧 `.co.kr` 分支，不能当作当前匿名路径的已验证证据 |
| CHZZK | `api.chzzk.naver.com` | 上游 `async_req` | 上游默认未迁移 | 仅公开匿名内容；需复核区域/CDN 行为 |
| TwitCasting | `twitcasting.tv`、`streamserver.php` | Reco Box 第一方匿名适配器 | 第一方已验证 | 仅公开房间；PR-06 明确传入 `verify=True`，不尝试登录保护房间 |
| SHOWROOM | `www.showroom-live.com` | 上游 `async_req` | 上游默认未迁移；上游存在 HTTP 播放地址降级逻辑 | 仅公开匿名内容；后续决定是否移除明文降级 |
| BIGO LIVE | `www.bigo.tv`、`ta.bigo.tv` | 上游 `async_req` | 上游默认未迁移 | 仅公开匿名内容；需公开样本复核 |
| 17LIVE | `wap-api.17app.co` | 上游 `async_req` | 上游默认未迁移 | 不通过年龄确认或访问控制；当前没有合格匿名样本 |
| LiveMe | `www.liveme.com`、`live.liveme.com` | 上游 `async_req` | 上游默认未迁移 | 公开匿名解析；Node.js 仅用于签名，不改变 TLS 边界 |
| Picarto | `ptvintern.picarto.tv` | 上游 `async_req` | 上游默认未迁移 | 仅公开、非受限频道；需公开样本复核 |
| Shopee Live | 区域 `live.shopee.*` | 上游 `async_req` | 上游默认未迁移 | 受区域和动态校验影响；不提交临时签名播放地址 |

## PR-06 结论

1. Reco Box 自己控制的 TwitCasting 匿名请求已有第一方策略入口，默认执行证书校验。
2. 其余通过锁定上游 `async_req` 的平台仍保留兼容性风险；本 PR 不把静态盘点误报为平台验证完成。
3. `spider.py` 中的 PopKornTV 登录函数和其他未被 Reco Box `Platform` 暴露的上游功能不属于本矩阵；它们不能在后续被误接入匿名流程。
4. 明文 HTTP 播放/辅助 Endpoint 不是“TLS 校验失败”的同一问题，后续需要单独的兼容性决策。

## 来源

- [Issue #1：Restore TLS certificate verification where possible](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1)
- [HTTPX SSL 文档](https://www.python-httpx.org/advanced/ssl/)
- [Requests API 文档](https://requests.readthedocs.io/en/stable/api/)
- [锁定的 DouyinLiveRecorder v4.0.7 async_http.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/http_clients/async_http.py)
- [Reco Box 公开平台样本调查](platform-live-samples-0.2.0.md)
