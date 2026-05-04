<#
.SYNOPSIS
Coastal Console Windows 一键安装脚本

.DESCRIPTION
🌊 Coastal Console - 基于DNA四维分析思想的可生长知识引擎
版本: 1.0.0
#>

<#
    颜色定义
#>
$RED = "`e[0;31m"
$GREEN = "`e[0;32m"
$YELLOW = "`e[1;33m"
$BLUE = "`e[0;34m"
$CYAN = "`e[0;36m"
$NC = "`e[0m" # 无颜色

<#
    日志函数
#>
function Write-Info { Write-Host "${BLUE}[INFO]${NC} $args" }
function Write-Success { Write-Host "${GREEN}[SUCCESS]${NC} $args" }
function Write-Warning { Write-Host "${YELLOW}[WARNING]${NC} $args" }
function Write-Error { Write-Host "${RED}[ERROR]${NC} $args" }

<#
    横幅
#>
function Print-Banner {
    Write-Host "${CYAN}"
    Write-Host "╔══════════════════════════════════════════════════════════╗"
    Write-Host "║                                                          ║"
    Write-Host "║  🌊 Coastal Console Windows 安装脚本                    ║"
    Write-Host "║  🔬 基于DNA四维分析思想的可生长知识引擎                  ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${GREEN}可生长 · 自指 · 进化 · 多维${CYAN}                           ║"
    Write-Host "║                                                          ║"
    Write-Host "╚══════════════════════════════════════════════════════════╝"
    Write-Host "${NC}"
}

<#
    检查系统
#>
function Check-System {
    Write-Info "检查系统环境..."

    # 检查 PowerShell 版本
    $psVersion = $PSVersionTable.PSVersion
    if ($psVersion.Major -lt 5) {
        Write-Error "需要 PowerShell 5.1 或更高版本"
        exit 1
    }
    Write-Info "PowerShell 版本: $psVersion"

    # 检查 Python
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Python 版本: $pythonVersion"
            # 检查版本 >=3.8
            $versionNum = [regex]::Match($pythonVersion, '\d+\.\d+').Value
            if ([version]$versionNum -lt [version]"3.8") {
                Write-Error "需要 Python 3.8 或更高版本"
                exit 1
            }
        }
        else {
            throw "未找到 Python"
        }
    }
    catch {
        Write-Error "未找到 Python，请先安装 Python 3.8+ 并添加到 PATH"
        exit 1
    }

    # 检查 pip
    try {
        & pip --version 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Info "找到 pip"
        }
    }
    catch {
        Write-Error "未找到 pip，请先安装 pip"
        exit 1
    }

    Write-Success "系统检查完成"
}

<#
    创建虚拟环境
#>
function Create-Venv {
    param([string]$venvName = "venv")

    Write-Info "创建 Python 虚拟环境: $venvName"

    if (Test-Path $venvName) {
        Write-Warning "虚拟环境已存在，跳过创建"
    }
    else {
        python -m venv $venvName
        if ($LASTEXITCODE -ne 0) {
            Write-Error "创建虚拟环境失败"
            exit 1
        }
    }

    # 激活虚拟环境
    $venvPath = Join-Path $venvName "Scripts\Activate.ps1"
    if (Test-Path $venvPath) {
        & $venvPath
        Write-Success "虚拟环境激活成功"
    }
    else {
        Write-Error "虚拟环境激活脚本不存在"
        exit 1
    }
}

<#
    升级 pip
#>
function Upgrade-Pip {
    Write-Info "升级 pip 和 setuptools..."
    python -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Error "升级 pip 失败"
        exit 1
    }
    Write-Success "pip 升级完成"
}

<#
    安装 Coastal Console
#>
function Install-Coastal {
    param([string]$installMethod = "pypi")

    Write-Info "安装 Coastal Console ($installMethod)..."

    switch ($installMethod) {
        "pypi" {
            pip install coastal-console[full]
        }
        "local" {
            if (Test-Path "setup.py") {
                pip install -e .
            }
            else {
                Write-Error "当前目录没有 setup.py 文件"
                exit 1
            }
        }
        "git" {
            if (Test-Path "coastal-console") {
                cd coastal-console
                pip install -e .
                cd ..
            }
            else {
                git clone https://github.com/cogniforge/coastal-console.git
                cd coastal-console
                pip install -e .
                cd ..
            }
        }
        default {
            Write-Error "无效的安装方式: $installMethod"
            exit 1
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error "安装 Coastal Console 失败"
        exit 1
    }
    Write-Success "Coastal Console 安装完成"
}

<#
    验证安装
#>
function Verify-Installation {
    Write-Info "验证安装..."

    try {
        $version = & coastal --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Coastal Console 安装成功: $version"
        }
        else {
            throw "命令执行失败"
        }
    }
    catch {
        Write-Error "安装失败，coastal 命令未找到"
        exit 1
    }

    # 测试基本功能
    Write-Info "测试基本功能..."
    & coastal --help 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "基本功能测试通过"
    }
    else {
        Write-Error "基本功能测试失败"
        exit 1
    }
}

<#
    后安装配置
#>
function Post-Install-Config {
    Write-Info "进行后安装配置..."

    # 创建用户目录
    $userDir = Join-Path $env:USERPROFILE ".coastal"
    $dirs = @("logs", "cache", "plugins", "templates")
    foreach ($dir in $dirs) {
        $path = Join-Path $userDir $dir
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path | Out-Null
        }
    }

    # 创建默认配置文件
    $configPath = Join-Path $userDir "config.json"
    if (-not (Test-Path $configPath)) {
        $config = @{
            version = "1.0.0"
            installed_at = (Get-Date).ToString("o")
            settings = @{
                theme = "ocean"
                log_level = "info"
                auto_update = $true
                telemetry = $false
            }
            paths = @{
                projects = "~/coastal-projects"
                cache = "~/.coastal/cache"
                logs = "~/.coastal/logs"
            }
        }
        $config | ConvertTo-Json -Depth 10 | Out-File $configPath -Encoding utf8
        Write-Success "配置文件已创建: $configPath"
    }

    # 创建示例项目目录
    $projectDir = Join-Path $env:USERPROFILE "coastal-projects\examples"
    if (-not (Test-Path $projectDir)) {
        New-Item -ItemType Directory -Path $projectDir | Out-Null
    }
}

<#
    显示完成信息
#>
function Show-Completion {
    Write-Host "`n${GREEN}"
    Write-Host "╔══════════════════════════════════════════════════════════╗"
    Write-Host "║                                                          ║"
    Write-Host "║  🎉 Coastal Console Windows 安装完成！                   ║"
    Write-Host "║                                                          ║"
    Write-Host "║  下一步操作：                                           ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${CYAN}1. 📖 查看帮助${GREEN}                                    ║"
    Write-Host "║     coastal --help                                      ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${CYAN}2. 🚀 初始化项目${GREEN}                                   ║"
    Write-Host "║     coastal init my-project                             ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${CYAN}3. 🔍 快速开始${GREEN}                                     ║"
    Write-Host "║     coastal analyze ./documents/                        ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${CYAN}4. 🌐 启动Web服务${GREEN}                                  ║"
    Write-Host "║     coastal serve                                       ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${CYAN}5. 🧬 让系统进化${GREEN}                                   ║"
    Write-Host "║     coastal evolve                                      ║"
    Write-Host "║                                                          ║"
    Write-Host "║  📁 配置文件: ~/.coastal/config.json${GREEN}              ║"
    Write-Host "║  📁 项目目录: ~/coastal-projects/${GREEN}                 ║"
    Write-Host "║                                                          ║"
    Write-Host "║  ${YELLOW}💡 提示: 运行 'coastal self-analyze' 检查系统状态${GREEN} ║"
    Write-Host "║                                                          ║"
    Write-Host "╚══════════════════════════════════════════════════════════╝"
    Write-Host "${NC}"
}

<#
    显示使用帮助
#>
function Show-Help {
    Write-Host "使用: .\install.ps1 [选项]"
    Write-Host ""
    Write-Host "选项:"
    Write-Host "  -h, --help            显示此帮助信息"
    Write-Host "  -m, --method METHOD   安装方法: pypi, local, git (默认: pypi)"
    Write-Host "  -e, --env ENV_NAME    虚拟环境名称 (默认: venv)"
    Write-Host "  -y, --yes             跳过确认提示"
    Write-Host "  --no-venv             不使用虚拟环境"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\install.ps1                     # 默认安装 (PyPI + 虚拟环境)"
    Write-Host "  .\install.ps1 --method git        # 从GitHub安装最新版"
    Write-Host "  .\install.ps1 --no-venv           # 不使用虚拟环境"
}

<#
    主函数
#>
function Main {
    # 默认参数
    $installMethod = "pypi"
    $venvName = "venv"
    $useVenv = $true
    $skipConfirm = $false

    # 解析参数
    for ($i = 0; $i -lt $args.Count; $i++) {
        switch ($args[$i]) {
            "-h" { Show-Help; exit 0 }
            "--help" { Show-Help; exit 0 }
            "-m" { $installMethod = $args[++$i] }
            "--method" { $installMethod = $args[++$i] }
            "-e" { $venvName = $args[++$i] }
            "--env" { $venvName = $args[++$i] }
            "-y" { $skipConfirm = $true }
            "--yes" { $skipConfirm = $true }
            "--no-venv" { $useVenv = $false }
            default { Write-Error "未知参数: $($args[$i])"; Show-Help; exit 1 }
        }
    }

    # 显示横幅
    Print-Banner

    # 确认
    if (-not $skipConfirm) {
        Write-Host "${YELLOW}即将安装 Coastal Console:${NC}"
        Write-Host "  安装方式: $installMethod"
        Write-Host "  虚拟环境: $($useVenv ? "是 ($venvName)" : "否")"
        Write-Host ""
        $confirm = Read-Host "是否继续? (Y/N)"
        if ($confirm -notmatch "^[Yy]$") {
            Write-Host "安装已取消"
            exit 0
        }
    }

    # 执行安装流程
    Check-System
    if ($useVenv) { Create-Venv $venvName }
    Upgrade-Pip
    Install-Coastal $installMethod
    Verify-Installation
    Post-Install-Config
    Show-Completion
}

# 运行主函数
Main $args