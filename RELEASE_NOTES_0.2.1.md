# Reco Box 0.2.1

## 本次维护

- 将项目、Python 包、PyInstaller 文件版本、Inno Setup 安装器和十语言 README 统一到 `0.2.1`。
- 将 Windows CI 的安装器验证扩展为：旧版 `0.2.0` 安装、`0.2.1` 覆盖安装、安装后 `--self-test`、静默卸载和安装根目录清理。
- 在覆盖安装与卸载前后检查外置 SQLite 中的应用配置、房间记录、录制历史、哨兵文件和 self-check 报告，确认用户数据不属于安装器清理范围。
- 为 Tag/手动发布流程加入安装包 SHA-256 校验和 GitHub Artifact Attestation。

## 发布边界

普通分支和 Pull Request CI 只做构建与验证，不创建公开 Release。正式发布流程只接受 `v*` Tag 或手动输入的既有 Tag，并在 attestation 成功后创建 Draft Release、校验资产后再发布。

本版本没有在本次维护任务中创建 Tag、执行正式 Release 或合并 Pull Request。安装包仍未进行商业代码签名；下载后应核对对应的 `.sha256.txt` 文件。

## 回滚

如需回滚本次代码，恢复到 `0.2.0` 的提交/安装包即可。升级验证使用的上一版安装包固定为公开 `v0.2.0` 资产，并在 CI 下载后核对其 SHA-256；它不会被修改。
