# ADR-20260905：Resolver 调度、并发限制与抖动

- 状态：已实现，等待 PR-09 审查和负责人验收
- 日期：2026-09-05
- 范围：Reco Box `0.3.0` / PR-09

## 背景

监控器当前每秒扫描房间，到期后直接把 Resolver 工作放入线程池。房间数量增加后，
相同检查间隔会造成请求 burst；Resolver 也不应通过修改 `QThreadPool.globalInstance()`
影响录制转换、ffprobe 和预览相关工作。路线要求先建立全局限制、平台限制、抖动和有界
重试，再进入错误分类和恢复状态机。

## 决策

1. 新增 `MonitoringScheduler`，集中计算成功检查、Resolver 重试、立即检查和外部指定
   延迟的截止时间。成功/Resolver 重试的默认抖动为 `0.9..1.1`，随机源可注入以保证
   测试可重复。
2. Resolver 重试继续保留已有的 60 秒上限；录制端通过 `schedule_delay` 传入已经决定的
   退避，不让监控器再次应用 Resolver 专用上限或随机抖动。
3. 新增 `ResolverRateLimitConfig` 和 `ResolverRateLimiter`。默认全局并发为 4，每个平台
   并发为 1，平台请求冷却为 1 秒；全局值、平台并发和平台冷却均可在构造时覆盖，现有
   全局设置页也允许用户在 1–32、1–16 和 0–3600 秒范围内保存这三项默认值。
4. `ResolverRateLimiter` 只在监控器所属线程中维护 `running_by_room`、
   `running_by_platform`、`last_request_by_platform` 和 `next_allowed_request`；permit
   在 Resolver 完成或失败时释放。设置页将三项默认值持久化到现有 `app_settings`，配置
   变更立即更新限流器和独立 Resolver 线程池，并按最近请求时间重算平台冷却截止时间；
   平台专属映射仍留给后续平台化配置任务。
5. `MonitoringCoordinator` 创建自己的 `QThreadPool`，只设置该池的最大线程数；录制端
   继续使用既有线程池，避免跨职责相互限速。

## 后果

- 相同平台的同时 Resolver 请求默认串行，平台间最多同时运行 4 个 Resolver；短间隔房间
  通过冷却和抖动分散请求。
- 由于当前默认平台冷却为 1 秒，快速返回的解析请求会比此前更保守；平台专项压力测试
  可以通过配置覆盖，而不需要改动监控算法。
- 这一步只约束“何时发起解析”，不分类网络/TLS/解析错误，也不判断录制是否卡顿；这些
  行为仍留给后续可靠性 PR。

## 恢复

回退 `scheduler.py`、`rate_limit.py`、`monitor.py`、相关测试和本 ADR/维护记录即可恢复
到 PR-08 的监控调度行为；不回退 TLS 适配器、上游源码、录制线程池或 `main`。

## 来源

- [PR-09 维护记录](../maintenance/2026-09-05-pr-09-scheduler.md)
- [项目仓库 AGENTS.md](../../AGENTS.md)
