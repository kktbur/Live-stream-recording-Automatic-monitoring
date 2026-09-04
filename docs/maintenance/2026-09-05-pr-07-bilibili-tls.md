# PR-07：Bilibili 第一方 TLS 迁移

- 状态：本地实施、专项验证、两轮审查问题修正和远程 Draft PR/Windows CI 完成；公开样本验证仍待完成
- 路线目标版本：`0.2.2`（本 PR 不修改当前包版本 `0.2.1`）
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`
- 本地分支：`codex/0.2.2-07-bilibili-tls`
- 本地基线：PR-06 本地提交 `51ead3b6fae2dcd9ff105855b370ac71602d060f`
- 本地实现提交：`f00f209`
- 远程恢复参考：PR-06 head `87e6d04b2d84295c9df429b50e64165d9258bfc1`
- 远程 Draft PR：[#11](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/11)，
  head `1eaaae4f4d60ee90b51380469896502d8b047e8a`，目标为 PR-06 分支，保持 open/draft。

## 范围

本轮继续执行 Issue #1 的逐平台迁移，选择请求边界清晰的 Bilibili。目标是让
Bilibili 房间状态、主播信息、标题和播放地址请求不再继承锁定上游
`async_req(..., verify=False)` 的默认值。

本轮不修改锁定的上游源码，不批量改变其他平台，不导入账号、Cookie、密码或
临时播放地址，也不声称 Issue #1 已整体关闭。

## 已实施

- 新增 `src/reco_box/bilibili.py`，由 Reco Box 自己创建 `httpx.AsyncClient`。
- 保留上游 v4.0.7 的公开接口顺序和质量映射：房间初始化、主播信息、H5 标题、
  旧版播放地址，旧接口没有可用结果时回退新版 `getRoomPlayInfo`。
- 请求显式传入第一方网络策略的 `verify`、代理、HTTP/2 和重定向设置；默认对
  `api.live.bilibili.com` 校验证书。
- 自动重定向改为逐跳处理，每一跳按目标 URL 重新计算 TLS 策略；支持 `b23.tv` 短
  链接解析，并限制其最终地址必须回到 Bilibili 直播 Host。
- `DouyinLiveRecorderResolver` 对 Bilibili 使用独立适配器，并在该路径上不再加载
  上游 Bilibili 解析函数。
- 适配器支持注入式 HTTP 客户端工厂，回归测试不访问真实直播平台，也不保存动态
  CDN 播放地址。
- 更新 README、PRIVACY、开源审计和平台网络安全矩阵，明确已验证范围与公开样本
  尚待验证的限制。

## 本地验证

- Bilibili、Resolver、网络策略专项测试：`29 passed`。
- 全量测试：`103 passed、2 failed、5 warnings`；两个失败仍是本机没有既有
  `runtime/ffmpeg/ffmpeg.exe`，分别影响预览解码和连带 self-check 前置项，不归因于
  PR-07；排除这两项后其余测试通过。
- `ruff check src tests`：通过。
- `python -m compileall -q src tests`：通过。
- `git diff --check`：通过。
- `uv lock --check --no-cache --python .venv-pr07/Scripts/python.exe`：通过。
- API 匿名拒绝、HTTP 403/500、非对象 JSON 和嵌套 codec 结构异常保持为离线结果；后续可靠性阶段再
  引入可观测的错误分类与重试策略。
- 最新固定点的独立 Standards/Spec 复审均无硬性问题；复审同时确认真实公开房间、动态
  CDN 可达性和短时录制仍未验证，因此不能据此关闭 Issue #1。
- 远程 Windows CI [#32](https://github.com/kktbur/Live-streaming-recording-Automatic-monitoring/actions/runs/33907554593)
  通过：锁文件、测试、Windows 构建、打包自检、十语言安装器构建及安装/升级/卸载冒烟均成功；
  诊断产物为 `RecoBox-installer-e2e-diagnostics-33907554593`，保留至 2026-09-11。
- 本轮尚未用真实公开直播间做网络/短时录制验证；该项必须由后续公开样本流程和
  Windows CI/人工验收单独确认。

## 验收门槛

- [x] Bilibili 请求从上游共享 `verify=False` 默认路径迁移到第一方客户端。
- [x] 默认策略传入 `verify=True`，精确 Host 例外和跨 Host 重定向逐跳校验有独立回归覆盖。
- [x] 代理、HTTP/2、重定向、`b23.tv` 短链接、质量映射和旧/新播放接口回退有离线回归覆盖。
- [x] 请求头不包含 Cookie；文档没有写入临时播放 URL 或凭据。
- [x] 匿名访问拒绝、HTTP 异常、非对象 JSON 和嵌套 codec 结构异常有回归覆盖。
- [x] 其他平台和锁定上游源码没有被本轮批量改写。
- [x] 最新固定点的独立 Standards/Spec 复审完成并记录结论。
- [x] Draft PR 和远程 Windows CI 完成并记录远程证据。

## 恢复与下一步

如果 Bilibili 迁移导致回归，只回退本 PR 新增提交，恢复到 PR-06 本地基线，
不改写 PR-06、PR-05 及更早分支，不触碰 `main`。远程发布保持 Draft，不创建
Tag、正式 Release 或合并 Pull Request。

下一步是在公开样本验证边界明确后，继续从矩阵选择下一个平台；Bilibili 完成
不等于 Issue #1 整体完成。
