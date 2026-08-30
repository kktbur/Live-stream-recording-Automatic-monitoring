# Reco Box 0.2.0 海外平台公开测试样本调查

调查日期：2026-08-30（Asia/Shanghai）

## 调查边界

- 只使用平台官方页面、平台官方公开接口，以及仓库内锁定的
  DouyinLiveRecorder v4.0.7 解析器源码。
- 不登录、不提供 Cookie、不绕过年龄、付费、私密、地区或其他访问控制。
- “已确认”只表示在调查时，官方页面或官方接口明确显示该房间正在公开直播；
  不代表该主播会一直开播。
- “候选”表示固定的官方房间页面可公开访问，但调查时无法从一手来源同时确认
  当前开播状态和可匿名播放地址。
- “无法确认”表示没有取得符合发布门槛的固定公开房间地址，或平台本身要求年龄/
  地区确认。此类平台不能据此宣称已经完成真实直播验证。

## 结果概览

> 后续实际录制复核见 `platform-validation-0.2.0.md`。调查时的“已确认”只代表
> 官方页面/API 当时显示正在直播。之后又找到了 BIGO LIVE、LiveMe 和 Shopee Live
> 的当前公开样本；是否真正通过仍以解析、短时录制和 MP4 封装结果为准。

| 平台 | 分类 | 建议测试地址 | 2026-08-30 一手证据 | 匿名访问边界 |
| --- | --- | --- | --- | --- |
| Twitch | 候选 | <https://www.twitch.tv/finalfantasyxiv> | 官方频道页可匿名访问并返回频道元数据；官方直播目录中也能看到该频道，但本次没有从无需凭据的官方状态接口取得同一时刻的开播状态 | 观看页无需登录；聊天等交互功能可能要求登录。部分频道可能有内容或地区限制 |
| SOOP Global | 候选 | <https://www.sooplive.com/taenaatakpoker> | 官方房间地址可访问，并重定向到官方 `station/taenaatakpoker` 页面；官方主页曾把该频道列为 Live，但 SOOP 官方状态 API 在当前网络发生 TLS 握手失败，无法做同一时刻复核 | 公开内容可匿名；成人、私密、登录保护或地区限制内容不得测试或绕过 |
| CHZZK | 已确认 | <https://chzzk.naver.com/live/c93cdb99760bc66b6f7f4462d95307ee> | 官方接口 [`/service/v1/lives?size=20`](https://api.chzzk.naver.com/service/v1/lives?size=20) 返回该频道 `status` 对应的直播列表数据、`adult:false`、频道名“올환”，并显示从 2026-08-27 持续开播的 24 小时直播 | 样本不是成人内容；仍可能因韩国境外 CDN/地区策略影响实际播放 |
| TwitCasting | 已确认 | <https://twitcasting.tv/TAXFRAUDALGDLY> | 官方英文首页 <https://en.twitcasting.tv/?r=home> 在调查时将该固定频道列为正在直播的 `24/7 DEEP STATIK LABS RADIO`；官方帮助明确说明观看直播无需注册/登录 | 只适用于公开直播；密码、群组、付费或 `login=true` 房间不得尝试登录 |
| SHOWROOM | 已确认 | <https://www.showroom-live.com/1126midorin> | 官方接口 [`/api/live/onlives`](https://www.showroom-live.com/api/live/onlives) 返回 `room_url_key:1126midorin`、`room_id:569829`、直播标题及公开 HLS 项 | 日本境外访问可能受网络/CDN 影响；样本本身未显示登录或年龄要求 |
| BIGO LIVE | 已通过 | <https://www.bigo.tv/id/695645820> | 当前公开房间完成匿名解析、20 秒 TS 录制和 MP4 封装；详情见实际验证报告 | 可能存在国家/地区分发差异；成人或私密房间不在测试范围 |
| 17LIVE | 无法确认 | 无合格样本 | 官方首页 <https://17.live/> 在未登录状态强制要求填写生日，并明确说明服务仅供 18 岁以上用户；没有取得不经过该年龄确认的固定公开房间样本 | 发布计划禁止通过年龄确认或访问控制，因此当前不能执行合格的匿名发布验证 |
| LiveMe | 已通过 | <https://www.liveme.com/v/17880688621118196521/index.html> | 当前公开房间完成匿名解析、20 秒 TS 录制和 MP4 封装，并验证安装包内置 Node.js 运行时 | 平台可能按地区返回不同推荐；直播状态随时变化 |
| Picarto | 已确认 | <https://www.picarto.tv/BooruGuru> | Picarto 官方公开接口 [`/api/v1/online`](https://api.picarto.tv/api/v1/online) 在调查时返回 `BooruGuru` 在线、69 名观众、`adult:false` 及公开缩略图；官方帮助也说明该接口用于获取所有在线频道 | 选用 `adult:false` 样本；私密或成人频道不在测试范围 |
| Shopee Live | 当前样本已确认，解析仍受阻 | 当前公开 Shopee SG/ID 会话 | 官方页面能确认正在直播并暴露可播放流，但锁定上游解析器的普通匿名请求被动态校验拒绝，不能算 Reco Box 通过 | 高度依赖区域站点、会话有效期和反滥用校验；0.2.0 保持 Beta |

## 已确认样本的建议优先级

这些样本可以立即交给 Reco Box 的真实解析与短时录制流程，但执行前仍需再次从官方
列表刷新，因为直播状态随时会改变：

1. CHZZK：`https://chzzk.naver.com/live/c93cdb99760bc66b6f7f4462d95307ee`
2. TwitCasting：`https://twitcasting.tv/TAXFRAUDALGDLY`
3. SHOWROOM：`https://www.showroom-live.com/1126midorin`
4. BIGO LIVE：`https://www.bigo.tv/id/695645820`
5. Picarto：`https://www.picarto.tv/BooruGuru`

其中 CHZZK、SHOWROOM 和 Picarto 的一手响应明确给出了直播状态；SHOWROOM 的响应
还直接包含 HLS 项。后续实际复核中 BIGO LIVE 已完成端到端通过，TwitCasting 仍为
间歇性通过，SHOWROOM 则在录制阶段收到 CDN HTTP 403。

## 候选样本

### Twitch

- 固定频道：<https://www.twitch.tv/finalfantasyxiv>
- 官方频道元数据可以匿名读取，页面明确属于官方 FINAL FANTASY XIV 频道。
- 当前网页元数据中的 “streams live” 文案不能单独证明此刻正在开播；发布测试时应先从
  Twitch 官方直播目录重新选择一个正在直播、无年龄/地区限制的频道，再立即运行解析。

### SOOP Global

- 固定频道：<https://www.sooplive.com/taenaatakpoker>
- 官方站点将该地址重定向为 `station/taenaatakpoker`，所以它是平台接受的正式频道地址。
- 当前环境访问 `api.sooplive.com` 时在 TLS 握手阶段失败，不能从官方接口确认 `isStream`
  或取得 master playlist。该问题可能是网络/区域/TLS 兼容性，而不是主播本身离线。
- 备用的可验证离线频道是 <https://www.sooplive.com/faker>；官方 SOOP 页面能够识别该
  频道，但这不满足“开播样本”的发布条件。

## 无法确认的准确阻塞

### 17LIVE

官方 Web 入口要求匿名访问者先输入生日，并声明 18+。按照 0.2.0 的发布边界，不能替
用户确认年龄，也不能写入浏览器年龄状态，因此没有合格的匿名测试地址。0.2.0 将其保留
为 Beta，并明确未通过真实录制验证。

### LiveMe

后续找到固定 `/v/<id>/index.html` 公开直播地址，并使用安装包内置 Node.js 运行时完成
匿名解析、20 秒 TS 录制、停止和 MP4 封装。该次测试通过，但房间状态和推荐地址仍具
时效性。

### Shopee Live

后续取得了当时正在直播的 Shopee SG 分享链接，并从官方印尼页面确认多条 `status:1`
会话及可播放流。可是 Shopee 网页客户端依赖动态请求校验和区域分发，锁定上游解析器的
普通匿名请求仍会被拒绝。0.2.0 不逆向或绕过这套保护，也不把网页端临时签名流地址提交
进 Git，因此只保留 Beta 标记并明确可能解析失败。

## 对 0.2.0 发布门槛的结论

后续真实测试已使 BIGO LIVE 和 LiveMe 完成端到端通过，也确认了 Shopee Live 的当前
公开会话与技术阻塞。用户批准 0.2.0 不再以十个平台全部通过为前提：所有新增海外平台
继续统一显示为 Beta，各自的通过、间歇性或阻塞状态在
`platform-validation-0.2.0.md` 中如实披露。发布说明不得把 Shopee Live 描述为稳定支持。

## 一手来源

- Twitch 官方频道：<https://www.twitch.tv/finalfantasyxiv>
- SOOP Global 官方频道：<https://www.sooplive.com/taenaatakpoker>
- CHZZK 官方直播列表接口：<https://api.chzzk.naver.com/service/v1/lives?size=20>
- TwitCasting 官方首页：<https://en.twitcasting.tv/?r=home>
- TwitCasting 官方观看帮助：<https://twitcasting.tv/helpcenter.php?pid=INDEX_HELP_VIEWER>
- SHOWROOM 官方在线列表：<https://www.showroom-live.com/api/live/onlives>
- BIGO LIVE 官方房间：<https://www.bigo.tv/id/695645820>
- BIGO LIVE 官方 PC 观看指南：<https://www.bigo.tv/blog/bigo-live-pc>
- 17LIVE 官方首页：<https://17.live/>
- LiveMe 官方房间：<https://www.liveme.com/v/17880688621118196521/index.html>
- Picarto 官方在线列表：<https://api.picarto.tv/api/v1/online>
- Picarto 官方 API 帮助：<https://help.picarto.tv/help/how-do-i-access-information-about-users/>
- Shopee Live 新加坡官方分享页（调查时有效）：
  <https://live.shopee.sg/share?from=live&session=1541377&share_user_id=30447702>
- 锁定上游源码：
  <https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/spider.py>
