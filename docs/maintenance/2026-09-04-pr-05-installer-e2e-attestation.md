# PR-05：Installer E2E 与发布来源证明

- 状态：实现、本地验证、独立审阅证据和最终远程 Windows CI 验证完成；Draft PR 等待负责人确认。
- 目标版本：`0.2.1`。
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`。
- 本地基线：PR-04 本地提交 `58da5128d57942f6316e7f8a2348c028028f7a7b`；PR-04 远程 head `1932ca883a2cbf39f94c49d390f4ef37acb16135`。
- 预期分支：`codex/0.2.1-05-installer-e2e-attestation`。

## 目标与范围

本次维护落实路线中的 Installer E2E 和发布供应链加强：

1. 将项目版本、锁文件、十语言 README 和发布说明推进到 `0.2.1`。
2. 在普通 Windows CI 中下载并固定校验公开的 `v0.2.0` 安装包，作为升级测试输入。
3. 在同一个安装根目录依次执行旧版安装、新版覆盖安装、安装后 `RecoBox.exe --self-test` 和静默卸载。
4. 在安装器操作前后检查外置 SQLite 数据库中的应用配置、房间记录和录制历史，以及哨兵文件和 self-check 报告，确认覆盖安装与卸载不会删除用户数据。
5. 在 Tag/手动发布工作流中校验安装包 SHA-256，生成 GitHub Artifact Attestation，并由独立的最小权限 job 创建 Draft Release 后发布。

普通 `push`/`pull_request` CI 仍不创建公开 Release；本轮不创建 Tag、不执行正式 Release、不合并 Pull Request。

## 既有发布输入

升级测试固定使用当前公开 `v0.2.0` 资产：

- 下载地址：[RecoBox-Setup-0.2.0.exe](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/releases/download/v0.2.0/RecoBox-Setup-0.2.0.exe)。
- 预期 SHA-256：`93ef84724582837e66a78c57e6da6d4eb7a4363171a4dbdf2129d1cbd01929bc`。
- 下载后由 CI 再次计算 SHA-256；不匹配即停止，不继续安装测试。

该固定 hash 是对现有公开资产的输入完整性保护，不等同于 GitHub Release 已启用 Immutable Releases。当前远程 `v0.2.0` Release 的 API 状态仍记录为 `immutable: false`，本次不修改仓库级设置。

## 实施文件

- `pyproject.toml`、`uv.lock`：发布版本 `0.2.1`。
- `README*.md`、`RELEASE_NOTES_0.2.1.md`：当前版本和维护边界说明。
- `tools/test_installer.ps1`：强制接收固定的旧版安装包，使用项目现有 `reco_box.storage.Database` 接口写入并读回测试配置、房间和录制历史，执行升级、安装后 self-check、卸载，并断言这些用户数据保留。
- `.github/workflows/ci.yml`：上一版安装包 hash 校验与普通 CI 安装器 E2E。
- `.github/workflows/release.yml`：Tag/手动触发、SHA 校验、attestation 和最小权限发布。
- `tests/test_ci_workflow.py`、`tests/test_project_version.py`、`tests/test_release_content.py`：工作流、版本单一来源和多语言内容回归契约。
- CI 安装目标使用 `RUNNER_TEMP` 隔离；失败时始终上传仅含安装器/卸载器日志的 7 天诊断 artifact，不上传用户数据库。

## 验收方式

远程 Windows CI 已在 [run #25](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33886308739) 逐步通过：锁文件检查、锁定依赖安装、版本检查、Ruff、完整测试、应用构建、打包 self-check、Inno Setup 安装器编译、固定旧版安装、当前版本覆盖安装、安装后 self-check、静默卸载、安装根目录清理，以及通过应用存储接口读回外置 SQLite 应用配置、房间记录、录制历史和其他用户数据保留。安装器测试没有旧版输入时会失败，不能使用当前版本替代。

首次 CI #18–#21 在工作区安装目标下暴露 Inno Setup 目标文件重命名失败（退出码 5，静默对话框默认 Abort 并回滚）；#22 因远程分支连续更新被取消。将安装目标隔离到 `RUNNER_TEMP` 后 #23、#24 和 #25 通过，说明该修正解决了 Runner 工作区路径上的文件锁/扫描竞争，不放宽安装器非零退出失败门槛。

Draft PR：[PR #9](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/9) 保持 open/draft；当前远程 head 和最新 CI 以 PR 页面为准。

未来正式发布还必须由 `release.yml` 在 `v*` Tag 或手动既有 Tag 上完成：构建 artifact、核对 SHA-256、使用 `actions/attest` 生成二进制来源证明，然后创建并发布 GitHub Release。attestation job 只拥有 `contents: read`、`id-token: write` 和 `attestations: write`；只有 publish job 拥有 `contents: write`。

## 已知本地限制

本机仓库没有提交 `runtime/ffmpeg/ffmpeg.exe` 和 `ffprobe.exe`，因此完整本地测试中预览解码及其连带 self-check 前置项不能有效完成。二进制运行时仍由 CI 下载并按 hash 校验；本地不伪造安装器 E2E，真实安装器结果以最终远程 Windows CI #25 为准。

## 恢复与回滚

如 PR-05 失败，先停止 Tag/Release 操作，沿用 PR-04 远程 head 作为恢复点，只回退 PR-05 新增提交；不改写 PR-04、PR-03 或 `main`。如果发现 `v0.2.0` 下载资产 hash 变化，应暂停升级测试并重新核对发布资产，而不是更新预期 hash 以绕过失败。

## 来源

- [GitHub Artifact Attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [`actions/attest` 官方说明](https://github.com/actions/attest)
- [Inno Setup 安装器命令行参数](https://jrsoftware.org/ishelp/topic_setupcmdline.htm)
- [Inno Setup 卸载器命令行参数](https://jrsoftware.org/ishelp/topic_uninstcmdline.htm)

