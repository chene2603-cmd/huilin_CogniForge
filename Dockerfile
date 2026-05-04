# 🌊 Coastal Console Docker 镜像
# 基于DNA四维分析思想的可生长知识引擎
# 版本: 1.0.0

# 基础镜像
FROM python:3.9-slim

# 维护者信息
LABEL maintainer="Coastal Console Team <team@coastalconsole.com>"
LABEL description="Coastal Console - 可生长知识引擎"
LABEL version="1.0.0"

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# 工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
COPY requirements-full.txt .

# 安装Python依赖
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# 复制项目文件
COPY . .

# 创建非root用户
RUN groupadd -r coastal && useradd -r -g coastal coastal

# 创建必要目录并设置权限
RUN mkdir -p /home/coastal/.coastal/{logs,cache,plugins,templates} && \
    mkdir -p /home/coastal/coastal-projects && \
    chown -R coastal:coastal /app /home/coastal

# 切换到非root用户
USER coastal

# 暴露端口
EXPOSE 8000

# 入口脚本
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# 默认命令
CMD ["coastal", "serve", "--host", "0.0.0.0", "--port", "8000"]