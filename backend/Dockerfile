# syntax=docker/dockerfile:1.4

# 第一阶段：构建阶段 - 安装所有依赖
FROM python:3.10-slim AS builder

WORKDIR /app

# 安装系统依赖（构建阶段需要的工具）
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并配置
RUN pip install --upgrade pip && \
    pip config set global.disable-pip-version-check true

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到 /app/packages 目录
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
    pip install --user -r requirements.txt

# 第二阶段：运行阶段 - 只包含运行时需要的文件
FROM python:3.10-slim AS runtime

WORKDIR /app

# 只安装运行时必需的系统依赖
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制已安装的 Python 依赖
COPY --from=builder /root/.local /root/.local

# 确保本地安装的包在 PATH 中
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY app.py .

# 设置环境变量
ENV COQUI_TOS_AGREED=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
