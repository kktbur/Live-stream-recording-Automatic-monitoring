# PR-06：TLS 网络矩阵与第一方策略接入

- 状态：本地实施、验证和审查修正完成；远程 Draft PR 与 Windows CI 待发布
- 路线目标版本：`0.2.2`（本 PR 不提前修改项目版本号，当前包版本仍为 `0.2.1`）
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`
- 基线：PR-05 远程 head `04ad3eb8634e8f0595f09353b4737fcb3481f79f`
- 预期分支：`codex/0.2.2-06-tls-network-matrix`
- 备份方式：保留本地 PR-05 分支提交 `2b3dfd14c9da4149dcd6c49bc9521f48f5a79d12` 和远程 PR-05 head 作为恢复快照；本轮不接触用户数据库、录制文件或构建产物。

## 范围

本轮对应 Issue #1 的第一阶段：盘点当前暴露平台的网络 Endpoint、匿名边界、
Resolver 请求路径和 TLS 状态，并为 Reco Box 自己控制的请求建立默认安全策略。

本轮不批量修改锁定上游所有平台的 `verify=False`，不新增账号登录、不导入 Cookie，
也不把明文 HTTP 播放地址伪装成 TLS 例外。

## 已实施

- 新增 `src/reco_box/network_policy.py`：默认校验 TLS；例外只能按平台和精确 Host 定义。
- `resolver.py` 的 TwitCasting 匿名页面和流地址请求通过第一方策略明确传入 `verify=True`。
- 新增 [Platform Network Security Matrix](../platform-network-security.md)。
- 更新 `README.md`、`PRIVACY.md` 和 `OPEN_SOURCE_AUDIT.md`，区分已接入策略的路径与仍待迁移的上游路径。
- 新增策略、精确 Host 例外和 TwitCasting 请求参数回归测试。
- 依据审查意见移除全局 `verify_tls=False` 入口，将数据类命名为
  `TLSEndpointOverride`，补上通过 Resolver 验证精确 Host 例外的回归测试，并修正
  TikTok、YouTube 和 SOOP Global 的矩阵路径描述。

## 当前结论

HTTPX 官方默认校验 HTTPS 证书，但锁定上游共享函数显式使用 `verify=False`；因此除
TwitCasting 第一方请求外，其他平台本轮只能记录为“上游默认未迁移”，不能宣称 Issue #1
已经整体关闭。后续必须按矩阵逐平台取得公开样本、TLS 兼容性和回归测试证据。

## 本地验证

- PR-06 专项测试：`18 passed`。
- 全量测试：`92 passed、2 failed、5 warnings`；两个失败均来自本机缺少既有的
  `runtime/ffmpeg/ffmpeg.exe`，分别影响预览解码和连带 self-check 前置项，不归因于
  本 PR。排除这两个 FFmpeg 前置项后：`92 passed、5 warnings`。
- Ruff：`src tests tools` 通过；`src tests tools` 编译检查通过；`git diff --check` 通过。
- 本地分支在验证完成后保持干净；具体提交链以 Git 历史和外层验证证据为准。

## 审查状态

第一轮独立 Standards/Spec 审查发现的备份记录缺失、命名误导、全局关闭入口、矩阵
路径不具体和 Resolver 例外路径缺少回归等问题均已修正。随后发起的复审任务在等待
窗口内未返回最终报告，因此不把它们记为“最终通过”；远程 Windows CI 仍是发布后的
机器验收门槛。

## 验收门槛

- [x] 平台矩阵覆盖当前 `Platform` 枚举和匿名访问边界。
- [x] 默认策略执行 TLS 校验，例外匹配精确 Host。
- [x] TwitCasting 第一方请求的回归测试确认 `verify=True`，精确 Host 例外路径也有回归测试。
- [ ] 远程 Windows CI 通过；本地普通测试已通过，FFmpeg 依赖项的本地限制已记录。
- [x] README、隐私说明和开源审计记录没有把部分迁移写成全部完成。

## 恢复与下一步

如果策略接线失败，只回退本 PR 新增提交，不改写 PR-05 及更早分支。下一步将从矩阵中
选择一个公开样本充分、请求边界清晰的平台，单独恢复其兼容路径的 TLS 校验。
