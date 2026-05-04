# 🌊 Coastal Console Makefile
# 基于DNA四维分析思想的可生长知识引擎

.PHONY: help install dev test lint format clean docker deploy

# 颜色定义
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20

# 显示帮助
help:
@echo ''
@echo '使用方法:'
@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
@echo ''
@echo '目标:'
@awk '/^[a-zA-Z\-\_0-9]+:/ { \
helpMessage = match(lastLine, /^## (.*)/); \
if (helpMessage) { \
helpCommand = substr($$1, 0, index($$1, ":")-1); \
helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
} \
} \
{ lastLine = $$0 }' $(MAKEFILE_LIST)
@echo ''

## 安装开发环境
install:
@echo "${GREEN}🚀 安装开发环境...${RESET}"
pip install -e ".[dev]"
pre-commit install
@echo "${GREEN}✅ 安装完成${RESET}"

## 安装生产环境
install-prod:
@echo "${GREEN}🚀 安装生产环境...${RESET}"
pip install -e .
@echo "${GREEN}✅ 安装完成${RESET}"

## 安装完整环境（包含AI功能）
install-full:
@echo "${GREEN}🚀 安装完整环境...${RESET}"
pip install -e ".[full]"
@echo "${GREEN}✅ 安装完成${RESET}"

## 启动开发服务器
dev:
@echo "${GREEN}🚀 启动开发服务器...${RESET}"
coastal serve --host 0.0.0.0 --port 8000 --reload

## 运行测试
test:
@echo "${GREEN}🧪 运行测试...${RESET}"
pytest -v --cov=coastal --cov-report=term-missing --cov-report=html

## 运行测试并生成覆盖率报告
test-cov:
@echo "${GREEN}🧪 运行测试并生成覆盖率报告...${RESET}"
pytest --cov=coastal --cov-report=html
@echo "${GREEN}📊 覆盖率报告: htmlcov/index.html${RESET}"

## 代码质量检查
lint:
@echo "${GREEN}🔍 代码质量检查...${RESET}"
flake8 coastal tests
mypy coastal
bandit -r coastal
safety check

## 代码格式化
format:
@echo "${GREEN}🎨 代码格式化...${RESET}"
black coastal tests
isort coastal tests
@echo "${GREEN}✅ 格式化完成${RESET}"

## 检查代码格式
check-format:
@echo "${GREEN}🔍 检查代码格式...${RESET}"
black --check coastal tests
isort --check-only coastal tests
@echo "${GREEN}✅ 格式检查完成${RESET}"

## 构建Docker镜像
docker-build:
@echo "${GREEN}🐳 构建Docker镜像...${RESET}"
docker build -t cogniforge/coastal-console:latest .

## 构建多架构Docker镜像
docker-buildx:
@echo "${GREEN}🐳 构建多架构Docker镜像...${RESET}"
docker buildx build \
--platform linux/amd64,linux/arm64 \
-t cogniforge/coastal-console:latest \
--push .

## 启动Docker开发环境
docker-dev:
@echo "${GREEN}🐳 启动Docker开发环境...${RESET}"
docker-compose --profile development up -d
@echo "${GREEN}✅ 开发环境已启动${RESET}"
@echo "${GREEN}🌐 Web界面: http://localhost:8000${RESET}"
@echo "${GREEN}🗃️  数据库: localhost:5432${RESET}"
@echo "${GREEN}🔴 Redis: localhost:6379${RESET}"

## 启动Docker生产环境
docker-prod:
@echo "${GREEN}🐳 启动Docker生产环境...${RESET}"
docker-compose --profile production up -d
@echo "${GREEN}✅ 生产环境已启动${RESET}"
@echo "${GREEN}🌐 Web界面: http://localhost:8000${RESET}"
@echo "${GREEN}📈 监控: http://localhost:9090${RESET}"

## 启动完整Docker环境
docker-full:
@echo "${GREEN}🐳 启动完整Docker环境...${RESET}"
docker-compose --profile production --profile monitoring --profile ai --profile vector up -d
@echo "${GREEN}✅ 完整环境已启动${RESET}"
@echo "${GREEN}🌐 Web界面: http://localhost:8000${RESET}"
@echo "${GREEN}📈 Prometheus: http://localhost:9090${RESET}"
@echo "${GREEN}📊 Grafana: http://localhost:3000${RESET}"
@echo "${GREEN}🤖 AI服务: http://localhost:8081${RESET}"

## 停止Docker环境
docker-down:
@echo "${GREEN}🛑 停止Docker环境...${RESET}"
docker-compose down
@echo "${GREEN}✅ Docker环境已停止${RESET}"

## 查看Docker日志
docker-logs:
@echo "${GREEN}📋 查看Docker日志...${RESET}"
docker-compose logs -f

## 重建Docker服务
docker-rebuild:
@echo "${GREEN}🔄 重建Docker服务...${RESET}"
docker-compose up -d --build
@echo "${GREEN}✅ Docker服务已重建${RESET}"

## 清理Docker
docker-clean:
@echo "${GREEN}🧹 清理Docker...${RESET}"
docker-compose down -v
docker system prune -f
@echo "${GREEN}✅ Docker已清理${RESET}"

## 数据库迁移
db-migrate:
@echo "${GREEN}🗃️  运行数据库迁移...${RESET}"
alembic upgrade head
@echo "${GREEN}✅ 数据库迁移完成${RESET}"

## 创建数据库迁移
db-revision:
@echo "${GREEN}🗃️  创建数据库迁移...${RESET}"
alembic revision --autogenerate -m "$(m)"
@echo "${GREEN}✅ 迁移文件已创建${RESET}"

## 回滚数据库迁移
db-downgrade:
@echo "${GREEN}↩️  回滚数据库迁移...${RESET}"
alembic downgrade -1
@echo "${GREEN}✅ 数据库回滚完成${RESET}"

## 启动数据库管理
db-shell:
@echo "${GREEN}🐘 启动数据库Shell...${RESET}"
docker-compose exec postgres psql -U coastal coastal

## 备份数据库
db-backup:
@echo "${GREEN}💾 备份数据库...${RESET}"
@mkdir -p backups
docker-compose exec -T postgres pg_dump -U coastal coastal > backups/coastal-$(shell date +%Y%m%d-%H%M%S).sql
@echo "${GREEN}✅ 数据库备份完成${RESET}"

## 恢复数据库
db-restore:
@echo "${GREEN}↩️  恢复数据库...${RESET}"
docker-compose exec -T postgres psql -U coastal coastal < backups/$(file)
@echo "${GREEN}✅ 数据库恢复完成${RESET}"

## 系统自我分析
self-analyze:
@echo "${GREEN}🔬 系统自我分析...${RESET}"
coastal self-analyze --detail
@echo "${GREEN}✅ 自我分析完成${RESET}"

## 系统进化
evolve:
@echo "${GREEN}🧬 系统进化...${RESET}"
coastal evolve --iterations 3
@echo "${GREEN}✅ 进化完成${RESET}"

## 构建文档
docs:
@echo "${GREEN}📚 构建文档...${RESET}"
sphinx-build -b html docs/source docs/build
@echo "${GREEN}✅ 文档构建完成: docs/build/index.html${RESET}"

## 启动文档服务器
docs-serve:
@echo "${GREEN}📚 启动文档服务器...${RESET}"
sphinx-autobuild docs/source docs/build --port 8001 --open-browser

## 打包发布
build:
@echo "${GREEN}📦 打包发布...${RESET}"
python -m build
@echo "${GREEN}✅ 打包完成${RESET}"

## 上传到PyPI
upload:
@echo "${GREEN}🚀 上传到PyPI...${RESET}"
twine upload dist/*
@echo "${GREEN}✅ 上传完成${RESET}"

## 清理构建文件
clean:
@echo "${GREEN}🧹 清理构建文件...${RESET}"
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf htmlcov/
rm -rf .pytest_cache/
rm -rf .mypy_cache/
rm -rf .coverage
rm -rf coverage.xml
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
@echo "${GREEN}✅ 清理完成${RESET}"

## 安全扫描
security:
@echo "${GREEN}🛡️  安全扫描...${RESET}"
bandit -r coastal
safety check
@echo "${GREEN}✅ 安全扫描完成${RESET}"

## 依赖更新
update-deps:
@echo "${GREEN}🔄 更新依赖...${RESET}"
pip install --upgrade pip
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in
@echo "${GREEN}✅ 依赖更新完成${RESET}"

## 检查依赖
check-deps:
@echo "${GREEN}🔍 检查依赖...${RESET}"
pipdeptree
@echo "${GREEN}✅ 依赖检查完成${RESET}"

## 启动所有服务
all: install docker-full
@echo "${GREEN}🚀 所有服务已启动${RESET}"

## 性能测试
benchmark:
@echo "${GREEN}⚡ 性能测试...${RESET}"
locust -f tests/performance/locustfile.py --headless -u 100 -r 10 -t 1m
@echo "${GREEN}✅ 性能测试完成${RESET}"

## 代码复杂度分析
complexity:
@echo "${GREEN}📊 代码复杂度分析...${RESET}"
radon cc coastal -a
@echo "${GREEN}✅ 复杂度分析完成${RESET}"

## 维护模式
maintenance-on:
@echo "${GREEN}🔧 启用维护模式...${RESET}"
touch maintenance.on
@echo "${GREEN}✅ 维护模式已启用${RESET}"

## 关闭维护模式
maintenance-off:
@echo "${GREEN}✅ 关闭维护模式...${RESET}"
rm -f maintenance.on
@echo "${GREEN}维护模式已关闭${RESET}"

## 查看系统状态
status:
@echo "${GREEN}📊 查看系统状态...${RESET}"
docker-compose ps
@echo ""
coastal status