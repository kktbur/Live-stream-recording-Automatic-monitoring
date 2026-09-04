# ADR-20260904：逐平台 TLS 网络策略

- 状态：Accepted for PR-06 第一阶段
- 日期：2026-09-04
- 范围：Reco Box `0.2.2` / PR-06

## 背景

锁定的 DouyinLiveRecorder v4.0.7 在共享异步 HTTP 客户端中把 `verify` 默认设为
`False`。这会让多个平台共用一个兼容性开关，无法知道具体是哪个 Endpoint 需要例外，
也无法在不改变其他平台的情况下逐个平台恢复证书校验。

HTTPX 和 Requests 的官方接口都把证书校验作为默认行为；明确传入 `verify=False`
才会关闭校验。因此 Reco Box 需要把第一方可控制的请求先接入自己的策略，再按平台
验证上游兼容性，而不是直接把整个上游目录的默认值一刀切掉。

## 决策

1. 新增 `reco_box.network_policy.NetworkPolicy`，默认执行 TLS 证书校验。
2. 兼容例外只能记录为平台 + 精确 Host + 原因，不能使用宽泛域名后缀或全局关闭。
3. PR-06 先把 Reco Box 自己实现的 TwitCasting 匿名请求接入该策略，并明确传入
   `verify=True`；匿名访问、Proxy 和请求 Header 行为保持不变。
4. 其他上游 `async_req` 平台暂不在这一 PR 中批量改默认值，先依据网络矩阵逐个平台
   取得公开样本和兼容性证据。
5. 明文 HTTP Endpoint、动态 CDN 播放地址和未暴露的上游登录函数分别记录，不把它们
   混同为普通 TLS 例外。

## 后果

- TwitCasting 的第一方匿名请求不再继承上游不安全默认值。
- 其余平台的中间人攻击风险仍存在，直到各自完成验证和迁移；隐私说明继续如实披露。
- 后续每个例外可以独立测试、审阅和回滚，不需要再次修改所有平台的共享默认值。

## 恢复

如果本 PR 的 TwitCasting 兼容性测试失败，只回退 PR-06 新增的策略接线和文档；不改写
PR-05、PR-04、PR-03 或 `main`。后续平台迁移沿用本 ADR 和矩阵作为独立恢复点。

## 来源

- [HTTPX SSL](https://www.python-httpx.org/advanced/ssl/)
- [Requests API](https://requests.readthedocs.io/en/stable/api/)
- [Issue #1](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1)
