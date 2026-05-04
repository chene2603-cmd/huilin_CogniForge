#!/bin/bash
# 🌊 Coastal Console 一键安装脚本
# 版本: 1.0.0

set -e  # 遇到错误退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 横幅
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║  🌊 Coastal Console 一键安装脚本                        ║"
    echo "║  🔬 基于DNA四维分析思想的可生长知识引擎                  ║"
    echo "║                                                          ║"
    echo "║  ${GREEN}可生长 · 自指 · 进化 · 多维${CYAN}                           ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查系统
check_system() {
    log_info "检查系统环境..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="Windows"
        log_error "Windows系统请使用PowerShell脚本"
        exit 1
    else
        OS="其他"
        log_warning "未知操作系统，可能不完全支持"
    fi
    
    log_info "操作系统: $OS"
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        log_info "Python版本: $PYTHON_VERSION"
        
        # 检查Python版本
        if [[ $(python3 -c "import sys; print('OK' if sys.version_info >= (3, 8) else 'FAIL')") == "FAIL" ]]; then
            log_error "需要Python 3.8或更高版本"
            exit 1
        fi
    else
        log_error "未找到Python3，请先安装Python 3.8+"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        log_info "找到 pip3"
    elif command -v pip &> /dev/null; then
        log_info "找到 pip"
    else
        log_error "未找到pip，请先安装pip"
        exit 1
    fi
    
    # 检查git
    if ! command -v git &> /dev/null; then
        log_warning "未找到git，部分功能可能受限"
    fi
    
    log_success "系统检查完成"
}

# 安装依赖
install_dependencies() {
    log_info "安装系统依赖..."
    
    if [[ "$OS" == "Linux" ]]; then
        # 检测Linux发行版
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS_ID=$ID
            
            case $OS_ID in
                ubuntu|debian)
                    log_info "检测到 $NAME，安装系统依赖..."
                    sudo apt-get update
                    sudo apt-get install -y \
                        build-essential \
                        python3-dev \
                        python3-venv \
                        libxml2-dev \
                        libxslt-dev \
                        libjpeg-dev \
                        zlib1g-dev \
                        libffi-dev \
                        libssl-dev \
                        curl \
                        wget
                    ;;
                fedora|centos|rhel)
                    log_info "检测到 $NAME，安装系统依赖..."
                    sudo dnf install -y \
                        gcc \
                        gcc-c++ \
                        python3-devel \
                        libxml2-devel \
                        libxslt-devel \
                        libjpeg-turbo-devel \
                        zlib-devel \
                        libffi-devel \
                        openssl-devel \
                        curl \
                        wget
                    ;;
                arch)
                    log_info "检测到 $NAME，安装系统依赖..."
                    sudo pacman -S --noconfirm \
                        base-devel \
                        python \
                        python-pip \
                        libxml2 \
                        libxslt \
                        libjpeg-turbo \
                        zlib \
                        libffi \
                        openssl \
                        curl \
                        wget
                    ;;
                *)
                    log_warning "不支持的系统: $OS_ID"
                    log_info "请手动安装: gcc, python3-dev, libxml2-dev, libxslt-dev, libjpeg-dev, zlib1g-dev"
                    ;;
            esac
        fi
    elif [[ "$OS" == "macOS" ]]; then
        log_info "检测到 macOS，安装系统依赖..."
        
        # 检查Homebrew
        if ! command -v brew &> /dev/null; then
            log_info "安装 Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        
        brew install \
            python@3.9 \
            libxml2 \
            libxslt \
            jpeg \
            openssl@1.1
    fi
    
    log_success "系统依赖安装完成"
}

# 创建虚拟环境
create_venv() {
    local venv_name="${1:-venv}"
    
    log_info "创建Python虚拟环境: $venv_name"
    
    if [ -d "$venv_name" ]; then
        log_warning "虚拟环境已存在，跳过创建"
    else
        python3 -m venv "$venv_name"
    fi
    
    # 激活虚拟环境
    if [ -f "$venv_name/bin/activate" ]; then
        source "$venv_name/bin/activate"
    elif [ -f "$venv_name/Scripts/activate" ]; then
        source "$venv_name/Scripts/activate"
    else
        log_error "无法激活虚拟环境"
        exit 1
    fi
    
    log_success "虚拟环境创建完成"
}

# 升级pip
upgrade_pip() {
    log_info "升级 pip 和 setuptools..."
    pip install --upgrade pip setuptools wheel
    log_success "pip 升级完成"
}

# 安装Coastal Console
install_coastal() {
    local install_method="$1"
    
    log_info "安装 Coastal Console ($install_method)..."
    
    case $install_method in
        "pypi")
            pip install coastal-console[full]
            ;;
        "local")
            if [ -f "setup.py" ]; then
                pip install -e .
            else
                log_error "当前目录没有 setup.py 文件"
                exit 1
            fi
            ;;
        "git")
            if [ -d "coastal-console" ]; then
                cd coastal-console
                pip install -e .
                cd ..
            else
                git clone https://github.com/cogniforge/coastal-console.git
                cd coastal-console
                pip install -e .
                cd ..
            fi
            ;;
        *)
            log_error "无效的安装方式: $install_method"
            exit 1
            ;;
    esac
    
    log_success "Coastal Console 安装完成"
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    if command -v coastal &> /dev/null; then
        VERSION=$(coastal --version 2>/dev/null || echo "未知")
        log_success "Coastal Console 安装成功: $VERSION"
    else
        log_error "安装失败，coastal 命令未找到"
        exit 1
    fi
    
    # 测试基本功能
    log_info "测试基本功能..."
    if coastal --help &> /dev/null; then
        log_success "基本功能测试通过"
    else
        log_error "基本功能测试失败"
        exit 1
    fi
}

# 后安装配置
post_install_config() {
    log_info "进行后安装配置..."
    
    # 创建用户目录
    mkdir -p ~/.coastal/{logs,cache,plugins,templates}
    
    # 创建默认配置文件
    if [ ! -f ~/.coastal/config.json ]; then
        cat > ~/.coastal/config.json << EOF
{
  "version": "1.0.0",
  "installed_at": "$(date -Iseconds)",
  "settings": {
    "theme": "ocean",
    "log_level": "info",
    "auto_update": true,
    "telemetry": false
  },
  "paths": {
    "projects": "~/coastal-projects",
    "cache": "~/.coastal/cache",
    "logs": "~/.coastal/logs"
  }
}
EOF
        log_success "配置文件已创建: ~/.coastal/config.json"
    fi
    
    # 创建示例项目目录
    mkdir -p ~/coastal-projects/examples
}

# 显示完成信息
show_completion() {
    echo -e "\n${GREEN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║  🎉 Coastal Console 安装完成！                          ║"
    echo "║                                                          ║"
    echo "║  下一步操作：                                           ║"
    echo "║                                                          ║"
    echo "║  ${CYAN}1. 📖 查看帮助${GREEN}                                    ║"
    echo "║     coastal --help                                      ║"
    echo "║                                                          ║"
    echo "║  ${CYAN}2. 🚀 初始化项目${GREEN}                                   ║"
    echo "║     coastal init my-project                             ║"
    echo "║                                                          ║"
    echo "║  ${CYAN}3. 🔍 快速开始${GREEN}                                     ║"
    echo "║     coastal analyze ./documents/                        ║"
    echo "║                                                          ║"
    echo "║  ${CYAN}4. 🌐 启动Web服务${GREEN}                                  ║"
    echo "║     coastal serve                                       ║"
    echo "║                                                          ║"
    echo "║  ${CYAN}5. 🧬 让系统进化${GREEN}                                   ║"
    echo "║     coastal evolve                                      ║"
    echo "║                                                          ║"
    echo "║  📁 配置文件: ~/.coastal/config.json${GREEN}              ║"
    echo "║  📁 项目目录: ~/coastal-projects/${GREEN}                 ║"
    echo "║                                                          ║"
    echo "║  ${YELLOW}💡 提示: 运行 'coastal self-analyze' 检查系统状态${GREEN} ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 显示使用帮助
show_help() {
    echo "使用: $0 [选项]"
    echo
    echo "选项:"
    echo "  -h, --help            显示此帮助信息"
    echo "  -m, --method METHOD   安装方法: pypi, local, git (默认: pypi)"
    echo "  -e, --env ENV_NAME    虚拟环境名称 (默认: venv)"
    echo "  -y, --yes             跳过确认提示"
    echo "  --no-venv             不使用虚拟环境"
    echo "  --system              系统级安装 (需要sudo)"
    echo
    echo "示例:"
    echo "  $0                     # 默认安装 (PyPI + 虚拟环境)"
    echo "  $0 --method git        # 从GitHub安装最新版"
    echo "  $0 --no-venv           # 不使用虚拟环境"
    echo "  $0 --system            # 系统级安装"
}

# 主函数
main() {
    # 默认参数
    INSTALL_METHOD="pypi"
    VENV_NAME="venv"
    USE_VENV=true
    SYSTEM_INSTALL=false
    SKIP_CONFIRM=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -m|--method)
                INSTALL_METHOD="$2"
                shift 2
                ;;
            -e|--env)
                VENV_NAME="$2"
                shift 2
                ;;
            -y|--yes)
                SKIP_CONFIRM=true
                shift
                ;;
            --no-venv)
                USE_VENV=false
                shift
                ;;
            --system)
                SYSTEM_INSTALL=true
                USE_VENV=false
                shift
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 显示横幅
    print_banner
    
    # 确认
    if [ "$SKIP_CONFIRM" = false ]; then
        echo -e "${YELLOW}即将安装 Coastal Console:${NC}"
        echo "  安装方式: $INSTALL_METHOD"
        echo "  虚拟环境: $([ "$USE_VENV" = true ] && echo "是 ($VENV_NAME)" || echo "否")"
        echo "  安装位置: $([ "$SYSTEM_INSTALL" = true ] && echo "系统级" || echo "用户级")"
        echo
        read -p "是否继续? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    
    # 检查系统
    check_system
    
    # 安装系统依赖
    install_dependencies
    
    # 处理虚拟环境
    if [ "$USE_VENV" = true ]; then
        create_venv "$VENV_NAME"
    elif [ "$SYSTEM_INSTALL" = true ]; then
        log_info "进行系统级安装..."
        if [ "$EUID" -ne 0 ]; then
            log_error "系统级安装需要sudo权限"
            exit 1
        fi
    fi
    
    # 升级pip
    upgrade_pip
    
    # 安装Coastal Console
    install_coastal "$INSTALL_METHOD"
    
    # 验证安装
    verify_installation
    
    # 后安装配置
    post_install_config
    
    # 显示完成信息
    show_completion
}

# 运行主函数
main "$@"