# 语音克隆系统

基于 Coqui YourTTS 的语音克隆系统，上传参考音频即可克隆音色生成语音。

## 系统要求

| 平台 | 支持 | 说明 |
|------|------|------|
| macOS (Intel) | ✅ | 完全支持 |
| macOS (Apple Silicon M1/M2/M3) | ✅ | 完全支持 |
| Windows 10/11 | ✅ | 需安装 Docker Desktop + WSL2 |
| Linux | ✅ | 完全支持 |

## How to Run

### macOS / Linux

```bash
# 启动项目
docker compose up --build -d

# 查看日志
docker compose logs -f

# 停止项目
docker compose down
```

### Windows

双击运行 `start.bat`，或在 PowerShell 中执行：

```powershell
docker compose up --build -d
```

## Services

| 服务 | 端口 | 说明 |
|------|------|------|
| frontend-user | 8081 | 用户前端界面 |
| backend | 5000 (内部) | 后端 API 服务 |

访问地址：http://localhost:8081

## 测试账号

无需登录，直接访问即可使用。

## 题目内容

帮我生成一个音频重现系统，功能是用户上传一段10秒左右的语音音频文件，输入一段文本内容，系统生成相同音色的语音音频。要求后端使用python，前端仅需要一个页面：上传音频，输入文本框，生成按钮，音频结果播放器。

---

## 目录结构

```
├── README.md                # 项目说明文档
├── docker-compose.yml       # Docker 编排配置
├── .gitignore              # Git 忽略文件配置
├── backend/                # 后端服务
│   ├── Dockerfile          # 后端 Docker 构建文件
│   ├── app.py              # Flask 应用主文件
│   └── requirements.txt    # Python 依赖
└── frontend-user/          # 用户前端
    ├── Dockerfile          # 前端 Docker 构建文件
    ├── index.html          # 前端页面
    └── nginx.conf          # Nginx 配置
```

## 功能说明

1. 上传一段约 10 秒的参考音频（WAV/MP3 等格式）
2. 输入要合成的文本内容
3. 点击生成按钮，系统将使用参考音频的音色朗读输入的文本
4. 在线播放或下载生成的语音

## 技术栈

- 后端：Python + Flask + Coqui TTS (YourTTS)
- 前端：HTML + CSS + JavaScript
- 部署：Docker + Nginx

## 语言支持说明

⚠️ **重要限制**：本系统使用的 YourTTS 模型仅支持以下语言：
- 英语 (English)
- 葡萄牙语 (Portuguese)
- 法语 (French)

**不支持中文**。如果输入中文文本，模型会将其当作英文字母发音处理，生成效果不佳。

建议使用英文文本进行语音克隆，例如：
- "Hello, this is a test of voice cloning technology."
- "The quick brown fox jumps over the lazy dog."

## 注意事项

- 首次启动时会自动下载 YourTTS 模型
- 语音克隆为 CPU 推理，生成速度较慢，请耐心等待
- 参考音频建议使用清晰的人声录音，时长约 10 秒
