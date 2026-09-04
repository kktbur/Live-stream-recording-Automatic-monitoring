# Platform Network Security Matrix

调查日期：2026-09-05（Asia/Shanghai）

## 调查边界

本表是 PR-06 第一阶段盘点、PR-07 Bilibili 迁移和 PR-08 YouTube 迁移结果。它根据 Reco Box 当前暴露的
`Platform` 枚举、第一方 Resolver 调用和锁定的 DouyinLiveRecorder v4.0.7 源码整理，
不使用账号、Cookie、密码或通知密钥，也不把临时播放地址写入仓库。

本轮的“未迁移”不是“平台证书一定无效”，而是该请求仍沿用上游
`async_req(..., verify=False)` 默认值，尚未完成 Reco Box 自己的逐平台兼容验证。
动态返回的 CDN 播放地址也需要在后续公开样本测试中单独记录。

## 状态定义

| 状态 | 含义 |
| --- | --- |
| 第一方已验证 | Reco Box 自己控制的请求明确传入 `verify=True`；截至 PR-08 覆盖 TwitCasting、Bilibili 和 YouTube 的匿名请求。 |
| 上游默认未迁移 | 请求经锁定上游的 `async_req`，当前默认 `verify=False`；不能宣称已恢复 TLS 校验。 |
| 直接客户端默认校验 | 上游直接创建 `httpx.AsyncClient` 且未覆盖 `verify`，按 HTTPX 默认行为校验；仍需平台公开样本验证。 |
| 明文 HTTP | URL 本身是 `http://`，没有 TLS 证书可校验；后续需单独决定是否能移除或替换。 |
| 不调用 | Reco Box 因匿名访问边界不会调用该登录接口。 |

## 当前暴露平台

| 平台 | 主要请求 Endpoint/Host | Resolver / 当前请求路径 | Anonymous | TLS Verify | Proxy | Tested |
| --- | --- | --- | --- | --- | --- | --- |
| 抖音 | `live.douyin.com`、`webcast.amemv.com`、`www.iesdouyin.com` | 上游 `async_req`；少数重定向辅助请求为直接 HTTPX | 仅匿名解析 | 上游默认未迁移；辅助请求为直接客户端默认校验 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| 快手 | `live.kuaishou.com`、`livev.m.chenzhongtech.com` | 上游 `async_req` | 仅公开匿名页面 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| Bilibili | `api.live.bilibili.com`；短链接入口 `b23.tv` | 第一方 `BilibiliResolver`：`room_init`、`Master/info`、`getH5InfoByRoom`、旧版 `playUrl`，失败时回退 `getRoomPlayInfo`；短链接逐跳解析 | 匿名、无 Cookie | 第一方已验证；默认 `verify=True` | 是，HTTP/HTTPS 且不含凭据 | 离线协议测试通过；公开样本/短录制待验证 |
| 小红书 | `www.xiaohongshu.com`、`app.xhs.cn`；媒体可能为 `live-source-play.xhscdn.com` | 上游 `async_req` | 仅匿名解析 | 上游默认未迁移；部分媒体地址可能为明文 HTTP | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| TikTok | 输入页面 `www.tiktok.com` / `tiktok.com`；播放 Host 从 `LiveRoom.liveRoom.streamData` 动态返回 | 页面请求经上游 `async_req`；播放地址由上游 `stream.py` 解析 | 匿名、不登录 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；地区和公开样本待验证 |
| YouTube | 输入页面 `youtube.com` / `youtu.be`；播放 Host 从 `streamingData.hlsManifestUrl` 动态返回 | 第一方 `YouTubeResolver`：页面播放器响应和 HLS 清单逐跳请求 | 仅公开匿名直播、无 Cookie | 第一方已验证；默认 `verify=True` | 是，HTTP/HTTPS 且不含凭据 | 离线协议测试通过；公开样本/短录制待验证 |
| 京东 | `lives.jd.com`、`api.m.jd.com` | 上游 `async_req` | 公开匿名解析 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；重定向、API 和播放地址待验证 |
| 淘宝 | `h5api.m.taobao.com` | Reco Box 在 Resolver 中拒绝调用 | 不调用 | 不调用 | 不调用 | 设计边界已测试；不做登录验证 |
| Twitch | `gql.twitch.tv`、`usher.ttvnw.net` | 上游 `async_req`；播放地址动态返回 | 仅公开频道 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| SOOP Global | 输入页面 `www.sooplive.com`；`api.sooplive.com`；`global-media.sooplive.com` | `.com` 路径由上游 `async_req` 请求频道/流信息和 HLS 清单 | 仅公开匿名内容 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| CHZZK | `api.chzzk.naver.com` | 上游 `async_req` | 仅公开匿名内容 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；区域/CDN 待验证 |
| TwitCasting | `twitcasting.tv`、`streamserver.php` | Reco Box 第一方匿名适配器 | 仅公开房间；不尝试登录保护房间 | 第一方已验证；明确传入 `verify=True` | 是，传入 `proxy_addr` | Resolver 回归通过；公开样本待验证 |
| SHOWROOM | `www.showroom-live.com` | 上游 `async_req` | 仅公开匿名内容 | 上游默认未迁移；存在 HTTP 播放地址降级逻辑 | 是，传入 `proxy_addr` | 静态盘点；明文降级待决策 |
| BIGO LIVE | `www.bigo.tv`、`ta.bigo.tv` | 上游 `async_req` | 仅公开匿名内容 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| 17LIVE | `wap-api.17app.co` | 上游 `async_req` | 不通过年龄确认或访问控制 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；暂无合格匿名样本 |
| LiveMe | `www.liveme.com`、`live.liveme.com` | 上游 `async_req` | 公开匿名解析 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| Picarto | `ptvintern.picarto.tv` | 上游 `async_req` | 仅公开、非受限频道 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；公开样本待验证 |
| Shopee Live | 区域 `live.shopee.*` | 上游 `async_req` | 区域和动态访问条件限制 | 上游默认未迁移 | 是，传入 `proxy_addr` | 静态盘点；不提交临时签名地址 |

## PR-06 结论

1. Reco Box 自己控制的 TwitCasting 匿名请求已有第一方策略入口，默认执行证书校验。
2. 其余通过锁定上游 `async_req` 的平台仍保留兼容性风险；本 PR 不把静态盘点误报为平台验证完成。
3. `spider.py` 中的 PopKornTV 登录函数和其他未被 Reco Box `Platform` 暴露的上游功能不属于本矩阵；它们不能在后续被误接入匿名流程。
4. 明文 HTTP 播放/辅助 Endpoint 不是“TLS 校验失败”的同一问题，后续需要单独的兼容性决策。

## PR-07 结论：Bilibili

1. `src/reco_box/bilibili.py` 接管 Bilibili 的房间状态、主播信息、标题和播放地址请求，
   不再调用锁定上游的 `async_req(..., verify=False)` 默认路径。
2. 第一方 `httpx.AsyncClient` 明确接收 `verify=self.network_policy.verify_for(...)`、代理、
   `http2=True` 和重定向设置；默认策略对 `api.live.bilibili.com` 执行证书校验。
3. 适配器不接收、不生成、不发送 Cookie 或账号凭据；播放地址是平台响应中的动态结果，
   不固化到代码、日志或维护文档。
4. 本轮测试是注入式离线协议测试，覆盖旧版播放接口、新版回退、质量选择、代理、短链接、
   HTTP/匿名错误的离线回退、匿名请求头和精确 Host 例外；它不等同于当前公开直播间的实网
 可用性验证，因此 Issue #1 仍未整体关闭。

## PR-08 结论：YouTube

1. `src/reco_box/youtube.py` 接管 YouTube 页面和 HLS 清单请求，不再调用锁定上游的
   `async_req(..., verify=False)` 默认路径。
2. 第一方 `httpx.AsyncClient` 明确接收 `verify=self.network_policy.verify_for(...)`、
   代理、`http2=True` 和手动重定向设置；页面重定向限制在 YouTube Host，清单和变体
   地址限制为 HTTP(S)。
3. 适配器不接收、不生成、不发送 Cookie 或账号凭据；播放地址是平台响应中的动态结果，
   不固化到代码、日志或维护文档。
4. 本轮测试是注入式离线协议测试，覆盖页面/清单、带宽排序、质量选择、`youtu.be`
   重定向、逐跳 TLS、HTTP/匿名错误和结构异常；它不等同于当前公开直播间的实网可用性
   验证，因此 Issue #1 仍未整体关闭。

## 来源

- [Issue #1：Restore TLS certificate verification where possible](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1)
- [HTTPX SSL 文档](https://www.python-httpx.org/advanced/ssl/)
- [Requests API 文档](https://requests.readthedocs.io/en/stable/api/)
- [锁定的 DouyinLiveRecorder v4.0.7 async_http.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/http_clients/async_http.py)
- [锁定的 DouyinLiveRecorder v4.0.7 Bilibili spider.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/spider.py)
- [HTTPX API 文档](https://www.python-httpx.org/api/)
- [Reco Box 公开平台样本调查](platform-live-samples-0.2.0.md)
