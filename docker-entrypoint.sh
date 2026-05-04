#!/bin/sh
# 🌊 Coastal Console Docker 入口点脚本
# 基于DNA四维分析思想的可生长知识引擎

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_banner() {
echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  🌊 Coastal Console - Docker 容器启动                    ║
║  🔬 基于DNA四维分析思想的可生长知识引擎                  ║
║                                                          ║
║  可生长 · 自指 · 进化 · 多维                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
}

wait_for_service() {
    local host="$1"
    local port="$2"
    local timeout="${3:-30}"
    log_info "等待服务: $host:$port"
    for i in $(seq $timeout); do
        nc -z "$host" "$port" && return 0
        sleep 1
    done
    log_error "服务超时: $host:$port"
    exit 1
}

main() {
    print_banner
    export COASTAL_HOME="/home/coastal/.coastal"
    export COASTAL_PROJECTS="/home/coastal/coastal-projects"
    mkdir -p "$COASTAL_HOME" "$COASTAL_PROJECTS"

    command="${1:-serve}"
    shift

    case "$command" in
        serve)
            log_info "启动 Web 服务..."
            exec uvicorn coastal.cli:app --host 0.0.0.0 --port 8000
            ;;
        *)
            exec coastal "$command" "$@"
            ;;
    esac
}

main "$@"
