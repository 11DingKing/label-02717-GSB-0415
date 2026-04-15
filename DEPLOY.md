# 音频克隆项目部署文档

## 项目简介

这是一个基于 Docker 的音频克隆项目，使用 Flask 后端和 Nginx 前端，支持语音克隆功能。

## 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB 可用内存
- 至少 10GB 可用磁盘空间

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd label-02717-GSB-0415
```

### 2. 一键启动

使用 Docker Compose 一键启动整个项目：

```bash
docker-compose up -d
```

### 3. 查看服务状态

```bash
docker-compose ps
```

### 4. 查看日志

查看所有服务日志：
```bash
docker-compose logs -f
```

查看特定服务日志：
```bash
docker-compose logs -f backend
docker-compose logs -f frontend-user
```

### 5. 访问应用

- 前端界面：http://localhost:8081
- 后端健康检查：http://localhost:5000/health

## 服务说明

### 后端服务 (backend)

- **镜像**：基于 Python 3.10-slim 多阶段构建
- **端口**：内部 5000（不对外暴露）
- **健康检查**：每 10 秒检查 `/health` 接口
- **数据卷**：
  - `voice_data`：音频数据存储
  - `tts_models`：TTS 模型缓存（避免重复下载）

### 前端服务 (frontend-user)

- **镜像**：基于 Nginx Alpine
- **端口**：8081:80
- **依赖**：等待后端服务健康检查通过后启动
- **反向代理**：`/api/` 请求自动转发到后端服务

## 常用命令

### 停止服务

```bash
docker-compose down
```

### 停止并删除数据卷（清空所有数据）

```bash
docker-compose down -v
```

### 重新构建镜像

```bash
docker-compose build --no-cache
```

### 重启服务

```bash
docker-compose restart
```

## 故障排查

### 后端启动慢

首次启动时需要下载 TTS 模型（约 200MB），请耐心等待。可以通过日志查看进度：

```bash
docker-compose logs -f backend
```

### 健康检查失败

检查后端服务是否正常启动：

```bash
docker-compose exec backend curl http://localhost:5000/health
```

### 清理磁盘空间

```bash
docker system prune -f
docker volume prune -f
```

## 架构说明

1. **多阶段构建**：后端 Dockerfile 采用两阶段构建，减小最终镜像体积
2. **健康检查**：后端配置健康检查，前端等待后端就绪后启动
3. **反向代理**：Nginx 作为反向代理，统一 API 入口
4. **数据持久化**：使用 Docker 卷存储模型和数据，避免重复下载
