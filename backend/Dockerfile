# syntax=docker/dockerfile:1.4
# 第一阶段：构建阶段，安装所有依赖
FROM python:3.10-slim AS builder

WORKDIR /app

# 安装系统依赖（仅在构建阶段需要的依赖）
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并配置
RUN pip install --upgrade pip && \
    pip config set global.disable-pip-version-check true

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到虚拟环境，方便后续拷贝
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

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

# 第二阶段：运行阶段，仅包含运行时所需的最小文件
FROM python:3.10-slim AS runtime

WORKDIR /app

# 安装运行时必需的系统依赖
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段拷贝虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 仅复制应用代码（不包含依赖文件）
COPY app.py .

# 设置环境变量
ENV COQUI_TOS_AGREED=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
