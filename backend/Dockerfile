# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖（合并 RUN 减少层数，使用国内镜像加速）
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并配置
RUN pip install --upgrade pip && \
    pip config set global.disable-pip-version-check true

# 复制依赖文件（单独复制以利用缓存）
COPY requirements.txt .

# 安装 Python 依赖（根据架构选择合适版本）
# x86_64: 使用轻量 CPU 版本（约 200MB）
# aarch64 (Apple Silicon): 使用 PyPI 标准版本（约 800MB）
RUN --mount=type=cache,target=/root/.cache/pip \
    ARCH=$(uname -m) && \
    echo "=== Building for architecture: $ARCH ===" && \
    if [ "$ARCH" = "x86_64" ]; then \
        echo "Installing PyTorch CPU-only version for Intel/AMD..." && \
        pip install torch==2.1.0+cpu torchaudio==2.1.0+cpu \
            --extra-index-url https://download.pytorch.org/whl/cpu; \
    else \
        echo "Installing PyTorch standard version for ARM64..." && \
        pip install torch==2.1.0 torchaudio==2.1.0; \
    fi && \
    pip install -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV COQUI_TOS_AGREED=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
