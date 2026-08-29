# Reco Box 0.1.3

首个公开测试版本，适用于 Windows x64。

## 下载

- `RecoBox-Setup-0.1.3.exe`：标准安装包
- `RecoBox-Setup-0.1.3.exe.sha256.txt`：SHA-256 校验文件

安装包尚未进行商业代码签名，Windows SmartScreen 可能显示“未知发布者”。请先核对 SHA-256：

`00CD2D11F6ED84C6D5B91C0E06DD3DA24F742C43907DE1E88AA65C7C15920219`

## 功能

- 卡片式直播间管理、搜索、筛选与排序
- 一键全部开始、全部暂停和批量删除
- 开播自动监控与手动立即检查
- 默认不分段，支持按分钟分段和数字序号命名
- TS 录制完成后无损封装为 MP4
- 主播 / 日期 / 场次开始时间的输出目录结构
- 录制历史、运行日志、托盘最小化与旧配置导入
- 本地运行，无 Reco Box 账号和遥测上传

## 平台状态

抖音、快手、Bilibili、小红书、TikTok、YouTube、京东已接入匿名解析；淘宝因锁定解析器需要登录会话而暂不启用。平台接口变化、网络环境和直播间类型都可能影响实际可用性。

## 发布安全

- 47 项自动测试通过。
- 打包程序离线自检通过。
- 公共安装包改用 FFmpeg 9.0.1 LGPL shared 构建；准确版本、源码与许可证见 `THIRD_PARTY_NOTICES.md`。
- 本地数据库、日志、配置、Cookie、导入备份、录制视频和私人路径均未进入发布集合。

FFmpeg 对应源码：
https://github.com/FFmpeg/FFmpeg/archive/e47273f4d9227152dcbf543cebaf9e2430ddbcc4.zip
