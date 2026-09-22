# Reco Box maintenance progress snapshot — 2026-09-22

状态：**Draft / validation active**。这是一份公开维护进度记录，不是正式 Release，也不代表
任务 14—16 已全部完成。

## 本次公开摘要

- Task 15 的短规模合成门槛已完成：10、50、100 个合成房间均通过 candidate-bound 检查。
- 验证运行器修正了一个收尾等待边界：独立 ffprobe worker 处于 `pending` 时，报告生成器继续等待，
  不再提前把未完成探测当成最终状态。
- 最新验证切片未修改 `src/reco_box/` 生产代码，候选安装包没有因为这个验证修正而重建。
- 两小时候选观察已启动，但在本快照生成时仍在运行，不能提前标记为通过。
- Task 14 的当前抖音/Bilibili 公开直播样本在匿名复核时均未提供可用直播流，因此真实平台链路仍是
  `NOT COVERED`，不是 `PASS` 或 `FAIL`。

## Candidate binding

| Item | Value |
| --- | --- |
| production candidate | `680e2fa1bb1b93b6e7f6ea0f90aa36dd454b63ed` |
| validation runner | `2b5ad15d2d228edd62a1eb11cae1882c0202c6d1` |
| package version | `0.2.1` |
| EXE SHA-256 | `4ee323310995e047fd62716834cca276012ad0c5f5e71921dfffba8a265fdc9d` |
| Installer SHA-256 | `a87e77c4b98a714bdf6b024e398bb2a41b0cf3e3a3d536e6f3fec9f5bdc7ba6a` |
| synthetic seed | `20260905` |

## Gate status

| Gate | Status | Current evidence boundary |
| --- | --- | --- |
| Task 15: 10/50/100 synthetic scale | **PASS** | 52 focused regressions passed; accepted reports had valid probes and final zero-state evidence |
| Task 15: 2-hour observation | **RUNNING** | 100 synthetic rooms, 7200-second target; final report not available at snapshot time |
| Task 14: real Douyin/Bilibili short recording | **NOT COVERED** | No current anonymous live room supplied a stream URL during the latest search window |
| Task 14: recording-time tray lifecycle | **OPEN** | Candidate-bound owner/manual black-box evidence remains required |
| Task 16 / formal Release | **CLOSED** | Must wait for Task 14 and Task 15 release gates |

## Public-release boundary

This snapshot intentionally excludes executable files, installers, SQLite databases, raw JSONL traces,
recording media, cookies, credentials, transient playback URLs, and local Windows paths. No `main` merge,
tag, or formal GitHub Release is included.

The next decision is made from the completed two-hour report. If it passes the resource, queue, fairness,
duplicate-recorder, media, and final-zero-state checks, the plan may enter the next long-observation gate.

