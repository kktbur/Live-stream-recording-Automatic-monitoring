# PR-08：YouTube 第一方 TLS 迁移

- 状态：本地实施、专项验证和文档更新完成；独立审查、远程 Draft PR、Windows CI
  和公开样本验证待完成
- 路线目标版本：`0.2.2`（本 PR 不修改当前包版本 `0.2.1`）
- 目标仓库：`kktbur/Live-stream-recording-Automatic-monitoring`
- 本地分支：`codex/0.2.2-08-youtube-tls`
- 本地恢复点：PR-07 本地最终工作树 `b105823`；远程 PR-07 最终 head
  `96a770d44dbc6526ebde06cbc8f4eb33d25ea805`

## 范围

本轮继续执行 Issue #1 的逐平台 TLS 迁移，选择 YouTube 页面和 HLS 清单这条请求边界。
目标是让 YouTube 不再继承锁定上游 `async_req(..., verify=False)` 的默认值，同时保持
当前匿名公开解析、代理、质量档位和离线结果语义。

本轮不修改锁定的上游源码，不导入账号、Cookie、密码或代理凭据，不绕过登录、年龄、
地区、付费或私密访问控制，也不声称 Issue #1 已整体关闭。

## 已实施

- 新增 `src/reco_box/youtube.py`，由 Reco Box 自己创建 `httpx.AsyncClient`，接管公开
  YouTube 页面和 HLS 清单请求。
- 请求显式传入第一方网络策略的 `verify`、代理、HTTP/2 和手动重定向设置；每一跳按
  目标 URL 重新计算 TLS 策略，页面重定向不得离开 YouTube Host。
- 支持 `youtube.com` 子域和 `youtu.be` 页面入口；清单及变体地址只接受 HTTP(S)，
  并按上游质量索引从带宽排序结果中选择录制地址。
- `DouyinLiveRecorderResolver` 对 YouTube 使用独立适配器，不再加载上游 YouTube
  解析函数；锁定的 vendor 源码和其他平台未批量修改。
- 适配器不接收、不生成、不发送 Cookie、账号凭据或代理凭据；动态清单和 CDN 地址
  只在内存中流转，不进入日志、源码或维护文档。
- 更新 README、PRIVACY、开源审计、平台网络安全矩阵、ADR、验收和当前状态文档。

## 本地验证

- YouTube、Resolver、网络策略专项测试：`31 passed`。
- 全量测试：`116 passed、2 failed、5 warnings`；两个失败仍是本机没有既有
  `runtime/ffmpeg/ffmpeg.exe`，分别影响预览解码和连带 self-check 前置项，不归因于
  PR-08；新增 YouTube 测试和其余测试均通过。
- `ruff check src tests`：通过。
- `python -m compileall -q src tests`：通过。
- `git diff --check`：通过。
- 测试覆盖匿名 HTTPX 参数、代理、HTTP/2、无 Cookie、质量选择、`youtu.be` 重定向、
  逐跳 TLS 策略、离开 YouTube Host 的重定向、HTTP 403/500、畸形页面、空清单和非
  HTTP(S) 清单地址。

## 证据边界

本轮测试使用注入式离线 HTTP 客户端，不访问真实 YouTube 页面、HLS 清单、动态 CDN 或
短时录制。真实公开房间、当前地区可达性、清单有效期和短时录制仍需后续公开样本流程
单独验收；因此本 PR 不关闭 Issue #1。

## 验收门槛

- [x] YouTube 页面和 HLS 清单请求从上游共享 `verify=False` 默认路径迁移到第一方客户端。
- [x] 默认策略传入 `verify=True`；精确 Host 例外和跨 Host 重定向逐跳校验有回归覆盖。
- [x] 代理、HTTP/2、手动重定向、`youtu.be` 入口、质量选择和 HLS 变体排序有离线回归覆盖。
- [x] 请求头不包含 Cookie；非 HTTP(S) 清单地址和离开 YouTube Host 的页面重定向被拒绝。
- [x] 匿名拒绝、HTTP 异常和结构异常归一化为既有离线结果，不改变监控状态机语义。
- [x] 其他平台和锁定上游源码没有被本轮批量改写。
- [ ] 独立 Standards/Spec 审查完成并记录最终结论。
- [ ] Draft PR 和远程 Windows CI 完成并记录远程证据。
- [ ] 真实公开 YouTube 房间、动态清单和短时录制完成单独验证。

## 恢复与下一步

如果 YouTube 迁移导致回归，只回退本 PR 新增适配器、Resolver 接线、测试和文档，
恢复到 PR-07 工作树，不改写 PR-07、PR-06 或 `main`。远程发布保持 Draft，不创建
Tag、正式 Release 或合并 Pull Request。

下一步应先完成本 PR 的独立审查、Windows CI 和公开样本验收；通过后再按路线继续
0.3.x 可靠性阶段。YouTube 迁移不等于 Issue #1 整体完成。
