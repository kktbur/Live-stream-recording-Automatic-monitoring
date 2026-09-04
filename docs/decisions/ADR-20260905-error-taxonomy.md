# ADR-20260905：Resolver 与录制错误类型分类

- 状态：已实现，等待 PR-10 最终审查和负责人验收
- 日期：2026-09-05
- 范围：Reco Box `0.3.0` / PR-10

## 背景

监控 Resolver 和录制端原先主要把失败转换为一段字符串。字符串能显示给用户，但无法稳定
驱动后续策略：限速应延长退避，磁盘不足不应自动重试，直播流过期应重新解析，TLS 或解析
错误则需要保留为可诊断的配置/上游问题。

## 决策

1. 在 `src/reco_box/errors.py` 建立 Resolver 和 Recording 两套独立异常层级，并用
   `ResolverErrorKind`、`RecordingFailureKind` 暴露稳定分类值。
2. 用 `RetryDirective` 表示未来恢复策略提示：`NO_RETRY`、`SHORT_BACKOFF`、
   `LONG_BACKOFF` 和 `RE_RESOLVE`。PR-10 只分类和传递提示，不改变 PR-09 的统一调度节奏。
3. 将 HTTP 429 归类为限速，将 401/403/407/451 归类为访问受限；HTTPX/Requests 超时归类为
   网络超时；TLS 异常链归类为 TLS 失败；结构/解析异常归类为解析失败；其余归类为未知失败。
4. 统一用安全错误文本进入 UI 和现有错误存储：折叠换行、限制长度，并从 URL 中移除用户信息、
   路径细节、查询参数和片段。
5. `ResolverWorker` 和 `RecordingManager` 保留结构化的最近失败对象，同时继续把兼容的字符串
   放入既有房间/录制展示；不在本轮增加数据库列或 Session 状态。
6. `RecordingFailure.Stalled` 只作为后续卡顿检测的稳定分类值预留；PR-10 不产生该类型，
   不增加 stall watchdog、状态转换或恢复动作。

## 后果

- 后续恢复逻辑可以按类型选择长退避、禁止重试或重新 resolve，而不再解析本地化字符串。
- 当前 UI 的错误文字仍可读，既有 Bilibili/YouTube 匿名请求失败转为 offline 的行为保持不变。
- 分类器对未知上游异常采用保守的 `UnknownResolverFailure`；在拥有真实样本前不伪造平台码率、
  限速阈值或恢复成功率。
- URL 安全清理会降低错误文字中的路径细节，但能避免临时播放地址和查询参数进入持久化错误
  字段或日志。

## 非目标

本 ADR 不定义卡顿检测、RecordingSession、恢复状态机、离线确认阈值、崩溃恢复、真实平台
限速测量或压力/故障注入；这些按路线继续拆分到后续 PR。

## 恢复

回退 PR-10 的错误类型模块、Resolver/监控/录制接线、相关测试和本 ADR/维护记录即可恢复到
PR-09 的字符串错误传递行为；不回退平台 TLS 适配器、上游源码或 `main`。

## 来源

- [PR-10 维护记录](../maintenance/2026-09-05-pr-10-error-taxonomy.md)
- [HTTPX exceptions 官方文档](https://www.python-httpx.org/exceptions/)
- [项目仓库 AGENTS.md](../../AGENTS.md)
