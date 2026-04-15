# syntax=docker/dockerfile:1.4

# 第一阶段：构建阶段 - 安装所有依赖
FROM python:3.10-slim AS builder

WORKDIR /build

# 安装系统依赖用于构建
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --upgrade pip && \
    pip config set global.disable-pip-version-check true

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到 /build/deps 目录
RUN --mount=type=cache,target=/root/.cache/pip \
    ARCH=$(uname -m) && \
    echo "=== Building for architecture: $ARCH ===" && \
    if [ "$ARCH" = "x86_64" ]; then \
        echo "Installing PyTorch CPU-only version for Intel/AMD..." && \
        pip install torch==2.1.0+cpu torchaudio==2.1.0+cpu \
            --extra-index-url https://download.pytorch.org/whl/cpu \
            --target /build/deps; \
    else \
        echo "Installing PyTorch standard version for ARM64..." && \
        pip install torch==2.1.0 torchaudio==2.1.0 --target /build/deps; \
    fi && \
    pip install -r requirements.txt --target /build/deps

# 第二阶段：运行阶段 - 只包含运行时需要的文件
FROM python:3.10-slim

WORKDIR /app

# 安装运行时需要的系统依赖
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制 Python 依赖
COPY --from=builder /build/deps /usr/local/lib/python3.10/site-packages

# 复制应用代码
COPY app.py .

# 设置环境变量
ENV COQUI_TOS_AGREED=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages

EXPOSE 5000

CMD ["python", "app.py"]
