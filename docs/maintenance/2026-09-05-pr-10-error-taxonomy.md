# PR-10：Resolver 与录制错误类型分类

- 状态：本地实现、专项验证、审查问题修正、Draft PR 和远程 Windows CI 完成；最终独立
  Standards/Spec 审查代理未返回，等待负责人验收。
- 路线目标：`0.3.0-03` 错误类型分类；本 PR 不修改当前包版本 `0.2.1`。
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`。
- 本地分支：`codex/0.3.0-02-error-taxonomy`。
- 本地代码固定点：`a581da1`；远程基础分支为 PR-09 分支的文档同步 head
  `c12808a6e8db262c866dcb09c47b04daa5f558e0`。

## 范围

此前监控 Resolver 和录制端主要把异常压缩为 `str(error)`，后续恢复逻辑无法区分访问受限、
限速、超时、TLS、解析、磁盘和 FFmpeg 失败。本轮建立统一分类和未来恢复提示，先保持现有
状态语义与重试节奏不变，不提前实现卡顿检测、Session 或恢复状态机。

## 已实施

- 新增 `src/reco_box/errors.py`：
  - `ResolverError` 下提供 `UnsupportedPlatform`、`AccessRestricted`、`RateLimited`、
    `NetworkTimeout`、`TLSFailure`、`ParseFailure` 和 `UnknownResolverFailure`；
  - `RecordingFailure` 下提供 `NetworkInterrupted`、`StreamExpired`、`DiskFull`、
    `FFmpegFailed`、`Stalled` 和 `ManualStop`；
  - 每个类型公开稳定的 `kind` 和未来恢复用 `retry_directive`，并不在本 PR 内自动执行该提示。
- `classify_resolver_error()` 按 HTTP 状态、HTTPX/Requests 超时、TLS 链、解析异常和未知异常
  归一化错误；429 映射为 `RateLimited`，401/403/407/451 映射为 `AccessRestricted`。
- `safe_error_text()` 限制消息长度、折叠换行，并将 URL、相对播放路径、查询字符串、Cookie、
  授权头或凭据降为安全表示；UI、事件和数据库写入边界均再次清理。
- Bilibili/YouTube 仍返回原有 offline 字典，但通过 `ResolvedStream.failure` 报告访问受限或
  限速分类；`ResolverWorker` 和 `MonitoringCoordinator` 保留每个房间的最近 Resolver 分类，
  同时保留字符串错误展示和旧的直接调用兼容性。
- 录制端将磁盘不足、FFmpeg 进程失败、转换失败和退出码映射为 `RecordingFailure`，保留最近
  分类；`ConversionResult` 额外携带可选的结构化失败对象，兼容调用者遗漏该对象时在管理器
  边界补齐分类；失败转换按 failed 状态持久化。
- `RecordingFailure.Stalled` 在本轮只是为路线图预留的稳定分类值；本 PR 不实现卡顿计时器、
  不发出 Stalled 状态，也不执行后续恢复动作，实际检测严格留到 `0.3.0-04`。
- Bilibili/YouTube 现有异常类接入共同分类基类，但其既有匿名请求失败转为 offline 的公共
  合约不变。

## 本地验证

- 错误分类、Resolver Worker、监控、录制转换和既有 Resolver 专项测试：`84 passed`。
- 全量测试：`171` 项中 `169 passed、2 failed、5 warnings`；两项失败仍是本机缺少既有
  `runtime/ffmpeg/ffmpeg.exe`，影响预览解码和连带 self-check 前置项，不归因于 PR-10。
- `ruff check src tests`：通过。
- `python -m compileall -q src tests`：通过。
- `git diff --check`：通过。

## 远程验证

- Draft PR [#14](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/14)
  仍为 open/draft，head 为 `5f62c48149f25d27d3a556f668f2ed5ef60f9f74`，目标为 PR-09 的
  文档同步分支；未合并。
- Windows CI [#41](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33929815223)
  已成功完成 lockfile、测试、Windows 构建、自检、安装/升级/卸载冒烟和诊断物上传阶段。
- 诊断物 `RecoBox-installer-e2e-diagnostics-33929815223`（artifact `9958232745`）仍未过期，
  SHA-256 为 `acde00b5b4ba47e67ccb2067b1f9aea22dc994b733033f6407d9fb2cb6e67486`，保留至
  2026-09-11。

## 证据边界

本 PR 证明异常可以被安全、确定性地分类并传递给监控/录制组件，不证明真实平台返回码的
长期分布，也不把 `retry_directive` 解释成已经完成的智能恢复。当前监控仍使用 PR-09 的
统一退避；后续 PR 才根据分类接入长退避、禁止重试、重新 resolve、卡顿和离线确认。

## 验收门槛

- [x] Resolver 和 Recording 两套错误层级覆盖路线图列出的类型。
- [x] HTTP 状态、HTTPX/Requests 超时、TLS、解析和未知异常有确定性分类测试。
- [x] 监控 Worker 和平台适配器传递结构化 Resolver 错误，录制端保留结构化失败对象。
- [x] 错误展示、事件和持久化消息做长度限制与 URL、查询参数、Cookie、授权信息清理。
- [x] 现有 Bilibili/YouTube 匿名失败的 offline 合约和 PR-09 统一重试节奏未改变。
- [x] 专项/全量测试、Ruff、compileall 和差异检查完成；FFmpeg 前置限制已记录。
- [ ] 独立 Standards/Spec 审查完成；本轮两个后续审查代理均未在等待窗口内返回最终报告。
- [x] Draft PR 和远程 Windows CI 完成；CI #41 已成功。

## 恢复与下一步

如果分类接线引起回归，只回退本 PR 的 `errors.py`、Resolver/监控/录制接线、测试和文档，
恢复到 PR-09 远程 head；不修改 `main`，不合并、不创建 Tag 或正式 Release。负责人验收后，
下一项严格进入 `0.3.0-04` Stall Detection。

## 来源

- [HTTPX exceptions 官方文档](https://www.python-httpx.org/exceptions/)
- [PR-09 维护记录](2026-09-05-pr-09-scheduler.md)
