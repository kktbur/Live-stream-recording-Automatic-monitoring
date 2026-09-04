# ADR-20260905：YouTube 第一方 TLS 请求边界

- 状态：已实现，等待 PR-08 审查和负责人验收
- 日期：2026-09-05
- 范围：Reco Box `0.2.2` / PR-08

## 背景

锁定的 DouyinLiveRecorder v4.0.7 通过共享异步请求函数访问 YouTube 页面和 HLS
清单，而该函数的 `verify` 默认值为 `False`。直接修改上游默认值会同时影响其他平台，
也无法单独验证 YouTube 的页面、重定向、清单、代理和质量行为。

## 决策

1. 新增 Reco Box 自己维护的 `YouTubeResolver`，接管 YouTube 的公开匿名页面和 HLS
   清单请求，不修改锁定上游源码。
2. 适配器对每个 HTTP(S) 请求使用 `httpx.AsyncClient`，明确传入
   `verify=self.network_policy.verify_for(Platform.YOUTUBE, url)`、代理、HTTP/2 和
   `follow_redirects=False`；手动处理重定向，并在每一跳重新计算策略。
3. 页面入口只接受 YouTube Host；`youtu.be` 可跳转到 YouTube 页面，但页面重定向离开
   YouTube Host 时拒绝。页面返回的清单和变体地址必须使用 HTTP(S)。
4. 保留上游公开解析的主播、直播状态、标题、HLS 清单和带宽排序行为；录制地址按照
   `OD/BD/UHD/HD/SD/LD` 的既有索引选择，缺少更低档位时使用最后一个可用变体。
5. 适配器不接收、不生成、不发送 Cookie 或账号凭据；动态清单和 CDN 播放地址只在
   内存中返回，不进入日志或维护文档。注入式客户端工厂用于离线、可重复的协议测试。
6. 对匿名拒绝、HTTP 错误和结构异常保留既有离线结果语义；详细错误分类、重试和
   卡顿恢复留给后续可靠性阶段，避免 TLS 迁移改变监控状态机。

## 后果

- YouTube 页面和清单请求默认恢复证书校验，且不会影响仍走上游共享函数的其他平台。
- 页面解析依赖公开 HTML 内嵌播放器响应，平台网页结构变化时需要维护适配器和测试。
- Issue #1 仍需其他平台逐一取得兼容性证据；真实公开 YouTube 房间、动态 CDN 和短时
  录制不由离线协议测试代替。

## 恢复

如果 YouTube 请求兼容性或回归测试失败，只回退 PR-08 新增适配器、Resolver 接线、
测试和相关文档，恢复到 PR-07；不改变上游目录、其他平台策略或 `main`。

## 来源

- [HTTPX API](https://www.python-httpx.org/api/)
- [锁定的 DouyinLiveRecorder v4.0.7 spider.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/spider.py)
- [锁定的 DouyinLiveRecorder v4.0.7 async_http.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/http_clients/async_http.py)
- [Issue #1](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1)
