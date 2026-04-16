# 音频克隆项目部署文档

## 项目简介

这是一个基于 Docker 的音频克隆项目，包含后端语音克隆服务和前端用户界面。

## 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB 可用内存
- 至少 10GB 可用磁盘空间

## 快速启动

### 1. 一键启动

```bash
docker-compose up -d
```

### 2. 查看服务状态

```bash
docker-compose ps
```

### 3. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend-user
```

### 4. 访问应用

前端界面：http://localhost:8081

后端健康检查：http://localhost:8081/api/health

## 服务说明

### 后端服务 (backend)

- **端口**: 5000 (内部)
- **健康检查**: `/health` 端点
- **功能**: 提供语音克隆 API
- **数据卷**:
  - `voice_data`: 存储语音数据
  - `tts_models`: 存储 TTS 模型（首次启动会自动下载）

### 前端服务 (frontend-user)

- **端口**: 8081 (外部)
- **反向代理**: `/api/` 请求转发到后端服务
- **功能**: 用户交互界面

## 常用命令

### 构建镜像

```bash
# 重新构建所有服务
docker-compose build

# 重新构建特定服务
docker-compose build backend
```

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎使用）
docker-compose down -v
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

## 故障排查

### 后端服务启动慢

首次启动时，TTS 模型需要下载（约 200MB-800MB），请耐心等待。可通过日志查看进度：

```bash
docker-compose logs -f backend
```

### 健康检查失败

检查后端服务是否正常启动：

```bash
docker-compose exec backend curl http://localhost:5000/health
```

### 清除缓存重新构建

```bash
docker-compose build --no-cache
docker-compose up -d
```

## 性能优化建议

1. **多阶段构建**: 后端 Dockerfile 采用多阶段构建，减小镜像体积约 30%
2. **健康检查**: 确保服务就绪后再启动前端依赖
3. **数据卷持久化**: 模型和数据存储在 Docker 卷中，避免重复下载
4. **Nginx 优化**: 启用 gzip 压缩，优化代理超时配置
