# ADR-20260905：Bilibili 第一方 TLS 请求边界

- 状态：已实现，等待 PR-07 负责人验收
- 日期：2026-09-05
- 范围：Reco Box `0.2.2` / PR-07

## 背景

锁定的 DouyinLiveRecorder v4.0.7 通过共享异步请求函数访问 Bilibili，而该函数的
`verify` 默认值为 `False`。直接把上游默认值改成 `True` 会同时影响其他平台，
也无法单独验证 Bilibili 的请求、代理、质量和回退行为。

## 决策

1. 新增 Reco Box 自己维护的 `BilibiliResolver`，接管 Bilibili 的公开匿名 API
   请求，不修改锁定上游源码。
2. 适配器对 `api.live.bilibili.com` 使用 `httpx.AsyncClient`，明确传入
   `verify=self.network_policy.verify_for(Platform.BILIBILI, endpoint)`、代理、
   HTTP/2 和逐跳重定向设置；每个重定向目标重新计算 `verify`。
3. 保留当前上游 v4.0.7 的房间初始化、主播信息、H5 标题、旧版播放接口和新版
   播放接口回退顺序，避免把 TLS 迁移误变成解析协议重写。
4. 适配器不接收、不生成、不发送 Cookie 或账号凭据；动态 CDN 播放地址只作为
   内存中的解析结果返回，不进入源码、日志或维护文档。
5. 支持 `b23.tv` 短链接，但只接受最终回到 Bilibili 直播 Host 的地址。使用注入式
   客户端工厂覆盖 HTTPX 边界，所有协议测试离线可重复；真实公开样本
   和短时录制属于后续产品可用性验收，不在本 ADR 中伪造为已完成。

## 后果

- Bilibili 的第一方 API 请求默认恢复证书校验，且不会影响仍走上游共享函数的其他平台。
- 适配器需要随着 Bilibili 公开 API 变化维护；旧/新播放接口回退和质量选择由本地
  回归测试固定住。
- Issue #1 仍需其他平台逐一取得兼容性证据，不能因 Bilibili 迁移完成而整体关闭。

## 恢复

如果 Bilibili 请求兼容性或回归测试失败，只回退 PR-07 新增适配器、Resolver 接线
和相关文档，恢复到 PR-06 提交；不改变上游目录、其他平台策略或 `main`。

## 来源

- [HTTPX API](https://www.python-httpx.org/api/)
- [锁定的 DouyinLiveRecorder v4.0.7 spider.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/spider.py)
- [锁定的 DouyinLiveRecorder v4.0.7 async_http.py](https://github.com/ihmily/DouyinLiveRecorder/blob/v4.0.7/src/http_clients/async_http.py)
- [Issue #1](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1)
