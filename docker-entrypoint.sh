#!/bin/bash
# 🌊 Coastal Console Docker 入口脚本
# 版本: 1.0.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 等待服务就绪（如有依赖服务）
wait_for_services() {
    log_info "等待依赖服务就绪..."
    
    # 这里可以添加等待数据库、缓存等服务的逻辑
    # 示例：等待数据库
    # until nc -z db 5432; do
    #     log_info "等待数据库连接..."
    #     sleep 2
    # done
    
    log_success "所有依赖服务已就绪"
}

# 初始化配置
init_config() {
    log_info "初始化配置..."
    
    # 创建必要目录
    mkdir -p /home/coastal/.coastal/{logs,cache,plugins,templates}
    mkdir -p /home/coastal/coastal-projects/examples
    
    # 如果配置文件不存在，创建默认配置
    if [ ! -f /home/coastal/.coastal/config.json ]; then
        cat > /home/coastal/.coastal/config.json << EOF
{
  "version": "1.0.0",
  "installed_at": "$(date -Iseconds)",
  "settings": {
    "theme": "ocean",
    "log_level": "${COASTAL_LOG_LEVEL:-info}",
    "auto_update": false,
    "telemetry": false
  },
  "paths": {
    "projects": "/home/coastal/coastal-projects",
    "cache": "/home/coastal/.coastal/cache",
    "logs": "/home/coastal/.coastal/logs"
  }
}
EOF
        log_success "默认配置文件已创建"
    fi
}

# 显示横幅
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║  🌊 Coastal Console Docker 容器                         ║"
    echo "║  🔬 基于DNA四维分析思想的可生长知识引擎                  ║"
    echo "║                                                          ║"
    echo "║  环境: ${GREEN}${COASTAL_ENV:-production}${BLUE}                                     ║"
    echo "║  版本: ${GREEN}1.0.0${BLUE}                                                ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 主函数
main() {
    show_banner
    wait_for_services
    init_config
    
    log_info "启动 Coastal Console..."
    log_info "执行命令: $*"
    
    # 执行传入的命令
    exec "$@"
}

# 运行主函数
main "$@"