# Podcast AI Assistant (播客飞书智能管家)

> 🚀 本地 GPU 驱动的极速播客总结与知识库自动同步工具

## 📖 项目简介

这是一个基于边缘计算（Edge Computing）架构设计的播客智能助手。通过将其部署在带有独立显卡的本地 Windows 主机上，它可以实现**零 API 成本、绝对隐私安全、并且超越云端 30 倍速度**的极速音频转写体验。

用户只需向自己的飞书机器人发送任意 B 站或小宇宙的播客链接，系统就会自动在后台下载音频、调用本地显卡进行 `Whisper` 极速转录，并使用 Map-Reduce 架构调用大模型提炼核心金句与时间轴，最终无感同步至本地 Obsidian 知识库。

## ✨ 核心亮点 (AI PM 视角)

- **边缘计算架构**：规避了云端缺乏廉价 GPU 的痛点。利用本地算力（RTX 显卡）进行 ASR 转写，1小时音频仅需1分钟。
- **Map-Reduce 长文本分块算法**：突破 LLM 常见的 8K/32K Context Window 限制。智能切分超长逐字稿，脱水降噪后再进行全局归约总结，保证了长播客大纲的结构完整性。
- **飞书 WebSocket 长连接**：抛弃了传统的 Webhook 隧道穿透（Ngrok/Cloudflare），通过官方底层长连接直接打通内网机器与云端飞书，极大降低了部署门槛。
- **无感知识库入库**：处理完成后的 Markdown 笔记自动遵循 Obsidian 格式归档，形成极佳的产品闭环。

## 🛠️ 技术栈
- **核心控制**：Python, FastAPI
- **消息通道**：飞书 Open API (lark-oapi WebSocket SDK)
- **下载引擎**：`yt-dlp` (支持自定义 UA 与 B站降级重试)
- **ASR 引擎**：`faster-whisper` (CTranslate2 框架，CUDA 加速)
- **LLM 大脑**：MIMO API (或任何兼容 OpenAI 格式的轻量级 API)

## 🚀 快速启动

1. 在飞书开发者后台创建企业自建应用，开启机器人与“长连接”订阅功能。
2. 配置 `.env` 文件：
```env
MIMO_API_KEY=你的大模型密钥
FEISHU_APP_ID=你的飞书应用ID
FEISHU_APP_SECRET=你的飞书应用密钥
```
3. 双击 `run_feishu_server.bat` 开启后台守候进程。
4. 在手机端向飞书机器人发送链接，坐等笔记生成。

## 🛡️ 异常处理
- 引入了全局异常捕获与临时文件的强一致性清理 (`try-finally`)，防止长时间运行导致 C 盘临时文件暴涨。
- `yt-dlp` 针对 CDN 阻断做了多级 Retry 机制。
