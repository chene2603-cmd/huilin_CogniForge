
# 🌊 Coastal Console - CogniForge 可生长知识引擎

基于 DNA 四维分析思想的自进化知识管理系统

## 项目介绍

- 自动文档分析与知识提取
- 多维质量评估与结构化编译
- 系统自指分析与自进化能力
- 内置 Web 管理界面
- 跨平台支持：Linux / macOS / Windows
- 容器化部署：Docker + Docker Compose

## 快速开始

# 安装
pip install -e .

# 初始化项目
coastal init my-knowledge-base

# 启动 Web 服务
coastal serve --host 0.0.0.0 --port 8000

访问 http://localhost:8000

## 核心命令

coastal init              创建知识库项目
coastal analyze           分析文档提取知识
coastal compile           编译生成结构化知识库
coastal serve             启动 Web 服务
coastal evolve            执行系统自进化
coastal self-analyze       系统自指诊断
coastal status            查看系统状态
coastal config            管理配置

## 部署方式

# Docker 开发环境
make docker-dev

# Docker 生产环境
make docker-prod

# 完整环境（含监控、AI、向量库）
make docker-full

## 技术栈

- 框架：Typer + Rich + FastAPI
- AI：OpenAI / Transformers / SpaCy
- 知识图谱：RDFLib / NetworkX
- 向量库：Chroma / Qdrant
- 存储：SQLite / PostgreSQL / Redis
- 工程：Makefile + pre-commit + CI/CD
