# 🌊 Coastal Console Docker镜像
# 版本: 1.0.0
# 基于DNA四维分析思想的可生长知识引擎

# 多阶段构建
# 阶段1: 构建阶段
FROM python:3.9-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt requirements-minimal.txt ./

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 安装依赖
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# 复制应用代码
COPY . .

# 安装Coastal Console
RUN pip install -e .

# 阶段2: 运行阶段
FROM python:3.9-slim

LABEL maintainer="CogniForge Team <contact@cogniforge.org>"
LABEL description="🌊 Coastal Console - 基于DNA四维分析思想的可生长知识引擎"
LABEL version="1.0.0"

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    poppler-utils \
    libjpeg-dev \
    zlib1g-dev \
    fonts-dejavu \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 创建非root用户
RUN groupadd -r coastal && useradd -r -g coastal -m -d /home/coastal coastal

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 创建工作目录
WORKDIR /app

# 复制应用代码
COPY --chown=coastal:coastal . .

# 切换用户
USER coastal

# 创建必要的目录
RUN mkdir -p /home/coastal/.coastal/{logs,cache,plugins,templates} \
    && mkdir -p /home/coastal/coastal-projects

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# 暴露端口
EXPOSE 8000

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV COASTAL_HOME=/home/coastal/.coastal
ENV COASTAL_PROJECTS=/home/coastal/coastal-projects
ENV LOG_LEVEL=info
ENV PORT=8000
ENV HOST=0.0.0.0

# 挂载卷
VOLUME ["/home/coastal/.coastal", "/home/coastal/coastal-projects"]

# 入口点脚本
COPY --chown=coastal:coastal docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]

# 默认命令
CMD ["serve"]
