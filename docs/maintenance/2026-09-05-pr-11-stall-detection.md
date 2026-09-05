# PR-11：录制卡顿检测

- 状态：本地实现、验证和独立复审完成；Draft PR/远程 Windows CI 待发布，负责人验收待完成
- 路线目标：`0.3.0-04` Stall Detection；本 PR 不修改当前包版本 `0.2.1`
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`
- 本地分支：`codex/0.3.0-04-stall-detection`
- 本地基线：PR-10 文档同步固定点 `fb000ee`
- 本地提交固定点：`1e1f233`（实现首提交 `47d5f38`）
- 当前文档同步 tip：`139f49b`

## 范围

录制进程仍处于运行状态，但录制目录中的文件大小在超过观察窗口后没有增长时，
将其识别为卡顿并执行已有的安全收尾路径。本轮只增加文件增长 watchdog、稳定的
`STALLED` 房间状态和 UI 提示；不提前引入 `RecordingSession`、恢复状态机、离线
确认阈值、崩溃恢复或压力/故障注入。

## 已实施

- `RecordingManager` 在 QProcess 发出 started 信号后，每秒读取当前 Session 目录的累计文件大小，
  记录最近增长时间。默认启动保护门槛为 30 秒、无增长阈值为 120 秒；首次判断必须同时满足
  进程运行至少 30 秒和距最近增长至少 120 秒，因此零输出场景最早约在进程启动后 120 秒触发；
  进程真正启动前不消耗卡顿计时。
- 触发后创建 `RecordingFailureKind.STALLED` 失败对象，房间进入 `RoomStatus.STALLED`，
  先向 FFmpeg 标准输入发送 `q`，等待 8 秒后沿用已有 terminate，再等待 3 秒后沿用已有
  kill 兜底；不会直接强杀正常收尾中的进程。
- 延时 terminate/kill 回调绑定原始 QProcess；如果旧进程已退出并开始新的重试，旧回调不会
  误操作新进程。自动收尾期间的 QProcess 错误也保留 `STALLED`，统一由完成回调进入重试。
- 卡顿停止沿用现有录制完成回调和重试调度，因而会进入既有的短退避重试路径；没有在本 PR
  新增智能恢复策略。手动停止优先级仍高于自动卡顿原因，用户在收尾期间主动停止不会被
  误判为自动失败。
- `RoomStatus.STALLED` 会阻止监控重复启动同一房间，保留录制筛选可见性，并在界面显示
  “卡顿收尾”；录制中的停止按钮、编辑、删除和立即检查按钮按进程收尾状态限制操作。
- `RoomListModel` 启动时会把没有对应 QProcess 的持久化 `STALLED` 瞬态标记恢复为 `OFFLINE`，
  保留原错误文字并允许已启用房间重新进入正常监控；这只是防止状态锁死，不实现完整崩溃恢复。
- 九种非中文语言的 TS/QM 翻译目录已同步新增状态文案，避免发布内容检查因 UI 文案漂移失败。

## 本地验证

- PR-11 定向测试：`28 passed`，覆盖纯判断边界、启动宽限期、进程状态、文件增长、
  `q` 收尾、状态更新、卡顿失败保留、干净 FFmpeg 退出码被卡顿原因覆盖，以及手动停止
  对自动卡顿原因的优先级。
- 全量测试：`179` 项中 `177 passed、2 failed、5 warnings`。剩余失败为本机没有准备
  `runtime/ffmpeg/ffmpeg.exe` 和 `runtime/ffmpeg/ffprobe.exe`，分别影响预览生成与带有
  FFmpeg 前置条件的 self-check；不归因于 PR-11，Windows CI 会下载并校验固定运行时。
- `ruff check src tests`：通过。
- `python -m compileall -q src tests`：通过。
- `git diff --check`：通过；翻译 QM 由项目虚拟环境中的 Qt Linguist 工具从 TS 重新生成。

## 验收门槛

- [x] 只对仍在运行、已过启动宽限期且文件持续无增长的录制触发卡顿检测。
- [x] 卡顿使用稳定 `Stalled` 分类值，并保留在现有录制失败、房间错误和重试路径中。
- [x] 发送 `q` 后等待 terminate/kill 兜底，且覆盖自动收尾与手动停止竞态。
- [x] `STALLED` 状态不会被监控器重复启动，UI 能显示、筛选并限制冲突操作。
- [x] 应用重启后不会因持久化 `STALLED` 标记永久锁住房间。
- [x] 定向测试、全量测试（前置条件限制已记录）、Ruff、compileall 和差异检查完成。
- [ ] Draft PR 发布并通过远程 Windows CI。
- [x] 独立 Standards/Spec 审查完成；最终复审未发现 P0/P1/P2。
- [ ] 负责人验收。

## 最新远程尝试

在负责人明确授权 `Main.qml` 和 `test_stall_detection.py` 后，这两个对象及 PR-11 文档对象已成功
创建到 GitHub 对象库；远程分支仍未更新。继续创建 `src/reco_box/domain.py` 时，连接器提示当前
授权未覆盖其余实现源码，因此停止上传，不创建缺文件提交或改用其他接口绕过。

## 证据边界

本 PR 证明本地模拟的“进程仍运行且文件无增长”会被确定性识别并安全收尾，
不证明任一真实平台的卡顿阈值最优，也不证明网络断流、播放器缓存或文件系统延迟在
所有编码器下都能被区分。后续 `RecordingSession`、恢复状态机、离线 hysteresis、
崩溃恢复和压力/故障注入仍需按路线单独验证。

## 恢复与下一步

若卡顿检测引起回归，回退本 PR 的状态枚举、增长追踪、收尾接线、UI、翻译、测试和文档，
恢复到 PR-10 文档同步固定点；不修改 `main`，不合并、不创建 Tag 或正式 Release。
负责人验收后，下一项为 `0.3.0-05` RecordingSession 建模与持久化边界。

## 来源

- [PR-10 维护记录](2026-09-05-pr-10-error-taxonomy.md)
- [FFmpeg 官方文档](https://ffmpeg.org/ffmpeg.html)
