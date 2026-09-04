# PR-09：Resolver 调度、并发限制与抖动

- 状态：本地实现、专项验证、独立 Standards/Spec 审查、远程 Draft PR 和 Windows CI
  已完成；100 房间压力/故障注入仍按路线留给后续任务
- 路线目标版本：`0.3.0`（本 PR 不修改当前包版本 `0.2.1`）
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`
- 本地分支：`codex/0.3.0-01-scheduler`，本地固定点 `141803d`
- 远程 Draft PR：[PR #13](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/13)，
  远程 head `7138a6adff74783e2233208691e57c65aa30ad17`
- 远程恢复点：PR-08 文档同步后的 head `159a6893e7555efbed9169cbd4b03346a1d82cb6`

## 范围

本轮开始执行 0.3.0 可靠性阶段的第一个子任务：让监控 Resolver 的启动节奏具备独立
的全局上限、平台级并发/冷却限制、每房间抖动和有界重试。目标是避免房间数量增加后
把所有请求集中在同一秒发出，也避免 Resolver 阻塞录制转换和媒体探测线程池。

本轮不实现错误类型层级、卡顿检测、RecordingSession、恢复状态机、离线确认阈值、
崩溃恢复或压力/故障注入套件；这些仍按路线顺序留给后续 PR。

## 已实施

- 新增 `src/reco_box/scheduler.py`：
  - 成功检查使用可注入随机源，在 `interval × 0.9..1.1` 内为每个房间生成独立截止时间；
  - Resolver 失败按 5→10→20→40→60 秒递增，并在抖动后把最终延迟限制为不超过 60 秒；
  - 立即检查和外部指定延迟分别保留明确入口，录制端已有的退避值不被再次截断或抖动。
- 新增 `src/reco_box/rate_limit.py`：
  - `ResolverRateLimitConfig` 将全局 Resolver 并发、平台并发和平台冷却配置化；默认分别
    为 `4`、每个平台 `1`、每个平台 `1` 秒；
  - `ResolverRateLimiter` 维护活动房间、平台活动计数、上次请求和下一次允许请求时间；
  - 三项默认值写入现有全局设置页（分别限制为 1–32、1–16 和 0–3600 秒），保存后立即
    应用于新的监控请求；热更新会按最近请求时间重算平台冷却截止时间；构造参数仍保留，
    便于测试和嵌入场景调参。
- `MonitoringCoordinator` 使用独立的 Resolver `QThreadPool`，不修改 Qt 全局线程池；
  解析完成或失败都会释放对应的 Resolver permit，原有 `.pool` 兼容属性保留。
- 新增调度、冷却、释放、独立线程池和监控整合回归测试。
- UI 证据：设置页截图使用合成数据和 `C:\\Demo\\Reco Box` 路径，未包含账号、Cookie、令牌、代理凭据或真实播放地址；见
  [PR-09 设置页截图](assets/pr-09-settings-dialog.png)。

## 本地验证

- 调度器、限流器、监控和设置接线专项测试：`27 passed`。
- 全量测试：`142 passed、2 failed、5 warnings`；两个失败仍是本机缺少既有
  `runtime/ffmpeg/ffmpeg.exe`，分别影响预览解码和连带 self-check 前置项，不归因于
  PR-09；新增测试和其余测试均通过。
- `ruff check src tests`：通过。
- `python -m compileall -q src tests`：通过。
- `git diff --check`：通过。

## 远程验证

- Windows CI [run #38](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33923911448)：通过。
- 该运行完成 lockfile 校验、测试、Windows 应用构建、打包自检、十语言安装器构建和安装/升级/卸载冒烟。
- 诊断工件 `RecoBox-installer-e2e-diagnostics-33923911448` 上传成功，保留至 2026-09-11。
- 独立 Standards/Spec 最终审查均无 P0/P1/P2/P3 阻塞问题；UI 截图已作为 PR 描述和维护记录证据。

## 证据边界

当前测试证明限流、冷却、抖动和线程池隔离的确定性逻辑，不证明 100 个房间的长时间
压力行为，也不证明真实平台服务端的限速阈值。平台默认冷却值是可调的初始保守值，
需要在后续 0.3.1 故障注入/压力测试中用脱机模型和受控样本复核。

## 验收门槛

- [x] 全局 Resolver 并发默认上限为 4，且不改动 `QThreadPool.globalInstance()`。
- [x] 平台并发默认上限、平台冷却、活动计数和释放路径有独立配置与测试。
- [x] 每个房间的成功检查使用可注入随机源生成 0.9..1.1 抖动；重试按 5→10→20→40→60 秒
  递增，抖动后的最终延迟不超过 60 秒。
- [x] 录制端传入的既有退避延迟不被监控调度器错误截断。
- [x] 监控整合测试证明全局 permit 会阻止多余 Resolver 启动，并在完成后释放。
- [x] 设置页限制值的持久化、边界拒绝、监控器热更新和平台冷却重算有回归测试。
- [x] 本地专项/全量测试、Ruff、compileall 和差异检查完成，FFmpeg 前置限制已记录。
- [x] 独立 Standards/Spec 审查完成并记录最终结论。
- [x] Draft PR 和远程 Windows CI 完成并记录远程证据。
- [ ] 受控 100 房间压力/故障注入验证完成；这属于 PR-09 后续可靠性验证，不在本轮伪造。

## 恢复与下一步

如果限流或抖动造成监控回归，只回退本 PR 的调度器、限流器、监控接线、测试和文档，
恢复到 PR-08 文档同步后的远程 head；不改写 PR-08、TLS 平台迁移或 `main`。远程发布
保持 Draft，不创建 Tag、正式 Release 或合并 Pull Request。

通过本轮独立审查和远程验证后，下一步是按路线进入 0.3.0-02 错误类型分类；不提前把
卡顿恢复、Session 或 Resolver 架构重构混入本 PR。
