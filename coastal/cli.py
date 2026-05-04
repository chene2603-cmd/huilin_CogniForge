#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌊 Coastal Console - CogniForge 命令行界面
继承DNA脚本的自指、进化、多维分析思想
将复杂的知识管理系统封装为简洁的CLI
"""

import sys
import os
import json
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

# 第三方依赖
try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.live import Live
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.text import Text
    from rich.prompt import Confirm, Prompt
    from rich import box
except ImportError:
    print("❌ 缺少必要依赖，请运行: pip install rich typer")
    sys.exit(1)

# 导入引擎模块
try:
    from engine.analyzer import CogniAnalyzer
    from engine.compiler import KnowledgeCompiler
    from engine.evolution import EvolutionEngine
except ImportError:
    # 如果引擎模块不存在，先创建基本结构
    pass

# 创建Rich控制台
console = Console()
app = typer.Typer(help="🌊 Coastal Console - 可生长知识引擎", rich_markup_mode="rich")

# 版本信息
VERSION = "1.0.0"
AUTHOR = "CogniForge Team"
DESCRIPTION = "基于DNA四维分析思想的智能知识管理系统"

class LogLevel(str, Enum):
    """日志级别枚举"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

class OutputFormat(str, Enum):
    """输出格式枚举"""
    JSON = "json"
    MARKDOWN = "markdown"
    TERMINAL = "terminal"
    HTML = "html"
    PDF = "pdf"

class Theme(str, Enum):
    """主题枚举"""
    DARK = "dark"
    LIGHT = "light"
    OCEAN = "ocean"
    FOREST = "forest"

class CoastalLogger:
    """增强的日志系统"""
    
    def __init__(self, log_file: str = "coastal.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # 颜色映射
        self.colors = {
            "debug": "dim blue",
            "info": "cyan",
            "warning": "yellow",
            "error": "red",
            "success": "green"
        }
        
        # 图标映射
        self.icons = {
            "debug": "🐛",
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO, 
            module: str = "Coastal", show_time: bool = True):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icon = self.icons[level.value]
        
        # 控制台输出
        if show_time:
            console.print(f"[{self.colors[level.value]}][{timestamp}][/] {icon} [{module}] {message}")
        else:
            console.print(f"{icon} [{self.colors[level.value]}][{module}][/] {message}")
        
        # 文件记录
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level.upper()}] [{module}] {message}\n")

logger = CoastalLogger()

def show_banner():
    """显示启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║  🌊 Coastal Console v1.0.0                              ║
    ║  🔬 CogniForge 知识引擎 - 基于DNA四维分析思想             ║
    ║                                                          ║
    ║  [bold cyan]可生长 · 自指 · 进化 · 多维[/bold cyan]                    ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    console.print(banner, justify="center")
    console.print()

def show_status():
    """显示系统状态"""
    status_table = Table(title="📊 系统状态", box=box.ROUNDED)
    status_table.add_column("模块", style="cyan")
    status_table.add_column("状态", style="green")
    status_table.add_column("版本", style="yellow")
    status_table.add_column("最后更新", style="dim")
    
    status_data = [
        ["核心引擎", "✅ 运行中", "1.0.0", datetime.now().strftime("%H:%M:%S")],
        ["知识库", "🔍 分析中", "0.9.1", "2026-05-04"],
        ["进化引擎", "🔄 待命", "1.2.0", "2026-05-03"],
        ["编译器", "⚡ 就绪", "1.1.0", "2026-05-04"],
    ]
    
    for row in status_data:
        status_table.add_row(*row)
    
    console.print(status_table)

def create_directory_structure(base_path: Path):
    """创建项目目录结构"""
    directories = [
        "sources",           # 原始资料
        "schema",           # 知识骨架
        "wiki",            # 可读输出
        "logs",            # 日志
        "cache",           # 缓存
        "exports",         # 导出
        "backups",         # 备份
        "plugins",         # 插件
        "templates",       # 模板
    ]
    
    console.print("[cyan]📁 创建目录结构...[/]")
    with Progress() as progress:
        task = progress.add_task("[cyan]创建目录...", total=len(directories))
        
        for dir_name in directories:
            dir_path = base_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            (dir_path / ".gitkeep").touch()  # 保留空目录
            progress.advance(task)
    
    # 创建配置文件
    config = {
        "version": VERSION,
        "created_at": datetime.now().isoformat(),
        "project_name": base_path.name,
        "directories": directories,
        "settings": {
            "auto_analyze": True,
            "auto_compile": False,
            "max_file_size": 100,  # MB
            "supported_formats": [".pdf", ".md", ".txt", ".py", ".html"],
            "theme": "ocean",
            "log_level": "info"
        }
    }
    
    config_path = base_path / "coastal.config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✅ 项目初始化完成: {base_path}[/]")

@app.command()
def init(
    project_name: str = typer.Argument(..., help="项目名称"),
    template: str = typer.Option("default", help="模板类型: default/research/engineering"),
    force: bool = typer.Option(False, "--force", "-f", help="强制覆盖已存在项目")
):
    """
    初始化新的知识库项目
    """
    show_banner()
    
    project_path = Path(project_name)
    
    if project_path.exists() and not force:
        if not Confirm.ask(f"📁 目录 '{project_name}' 已存在，是否覆盖？"):
            console.print("[yellow]❌ 初始化取消[/]")
            return
        shutil.rmtree(project_path)
    
    with console.status("[bold green]初始化项目中...") as status:
        # 创建目录结构
        create_directory_structure(project_path)
        
        # 复制模板文件
        if template != "default":
            status.update(status="[bold green]加载模板...")
            # 这里可以添加模板复制逻辑
            logger.log(f"使用模板: {template}", LogLevel.INFO, "Init")
        
        # 创建示例文件
        status.update(status="[bold green]创建示例文件...")
        example_dir = project_path / "sources" / "examples"
        example_dir.mkdir(exist_ok=True)
        
        # 创建README示例
        readme_content = f"""# {project_name} 知识库

## 项目概述
这是由Coastal Console自动创建的知识库。

## 目录结构
- `sources/` - 原始资料
- `schema/` - 知识骨架
- `wiki/` - 可读输出
- `logs/` - 日志文件
- `exports/` - 导出文件

## 快速开始
1. 添加文档到 `sources/` 目录
2. 运行分析: `coastal analyze`
3. 编译知识库: `coastal compile`
4. 查看结果: `coastal serve`
5. 让系统进化: `coastal evolve`

## 支持的格式
- PDF文档
- Markdown文件
- 文本文件
- 代码文件
- HTML网页

> 创建于: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        (example_dir / "README.md").write_text(readme_content, encoding="utf-8")
        
        # 创建配置文件示例
        config_example = {
            "name": "示例配置",
            "description": "这是一个示例配置，展示了如何扩展Coastal Console",
            "extensions": {
                "custom_analyzer": "path.to.your.analyzer",
                "custom_formatter": "path.to.your.formatter"
            }
        }
        
        (project_path / "templates" / "example.config.json").write_text(
            json.dumps(config_example, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )
    
    console.print(Panel.fit(
        f"[bold green]🎉 项目 '{project_name}' 初始化完成！\n\n"
        f"[cyan]📁 位置:[/] {project_path.absolute()}\n"
        f"[cyan]📄 配置:[/] {project_path}/coastal.config.json\n"
        f"[cyan]📖 示例:[/] {project_path}/sources/examples/\n\n"
        f"[yellow]👉 下一步:[/]\n"
        f"1. 添加文档到 sources/ 目录\n"
        f"2. 运行 [bold]coastal analyze[/] 开始分析\n"
        f"3. 运行 [bold]coastal serve[/] 启动本地服务",
        title="项目创建成功",
        border_style="green"
    ))

@app.command()
def analyze(
    path: str = typer.Argument(".", help="要分析的路径"),
    content_type: Optional[str] = typer.Option(None, "--type", "-t", 
                                              help="指定内容类型: tech/paper/business/note/auto"),
    recursive: bool = typer.Option(True, "--recursive", "-r", help="递归分析子目录"),
    output_format: OutputFormat = typer.Option(OutputFormat.TERMINAL, "--format", "-f", 
                                               help="输出格式"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出"),
    batch: bool = typer.Option(False, "--batch", "-b", help="批量模式")
):
    """
    分析文档并提取知识
    """
    show_banner()
    
    analyze_path = Path(path)
    if not analyze_path.exists():
        console.print(f"[red]❌ 路径不存在: {path}[/]")
        return
    
    # 初始化分析器
    logger.log("初始化分析引擎...", LogLevel.INFO, "Analyze")
    analyzer = CogniAnalyzer(name="Coastal Analyzer")
    
    # 收集要分析的文件
    files_to_analyze = []
    if analyze_path.is_file():
        files_to_analyze = [analyze_path]
    else:
        # 递归查找文件
        patterns = ["*.md", "*.txt", "*.py", "*.json", "*.yaml", "*.yml", "*.pdf"]
        for pattern in patterns:
            files_to_analyze.extend(analyze_path.rglob(pattern) if recursive else analyze_path.glob(pattern))
    
    if not files_to_analyze:
        console.print("[yellow]⚠️ 未找到可分析的文件[/]")
        return
    
    console.print(f"[cyan]🔍 找到 {len(files_to_analyze)} 个文件进行分析...[/]")
    
    results = []
    failed_files = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("分析中...", total=len(files_to_analyze))
        
        for file_path in files_to_analyze:
            try:
                # 读取内容
                if file_path.suffix == ".pdf":
                    content = f"[PDF文档] {file_path.name}"
                    # TODO: 实现PDF解析
                else:
                    content = file_path.read_text(encoding="utf-8")
                
                # 分析内容
                progress.update(task, description=f"分析: {file_path.name[:30]}...")
                result = analyzer.analyze_content(content, content_type or "auto")
                
                # 添加文件信息
                result["file_path"] = str(file_path)
                result["file_size"] = file_path.stat().st_size
                result["file_type"] = file_path.suffix
                
                results.append(result)
                
                if verbose:
                    # 显示单文件分析结果
                    self._display_single_result(result)
                
            except Exception as e:
                failed_files.append((file_path, str(e)))
                logger.log(f"分析失败: {file_path} - {e}", LogLevel.ERROR, "Analyze")
            
            progress.advance(task)
    
    # 显示总结
    self._display_analysis_summary(results, failed_files, output_format)
    
    # 保存结果
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path("analysis_results") / f"analysis_{timestamp}.json"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "analyzed_at": timestamp,
                    "total_files": len(files_to_analyze),
                    "successful": len(results),
                    "failed": len(failed_files)
                },
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]📁 分析结果已保存: {output_file}[/]")
    
    logger.log(f"分析完成: {len(results)} 成功, {len(failed_files)} 失败", 
               LogLevel.SUCCESS, "Analyze")

def _display_single_result(self, result: dict):
    """显示单个文件的分析结果"""
    console.print(f"\n[bold cyan]📄 文件: {result.get('file_path', 'Unknown')}[/]")
    
    # 基本信息
    table = Table(show_header=False, box=box.SIMPLE)
    table.add_column("属性", style="cyan")
    table.add_column("值")
    
    table.add_row("ID", result.get("id", "N/A"))
    table.add_row("类型", result.get("type", "N/A"))
    table.add_row("分析时间", result.get("timestamp", "N/A"))
    
    console.print(table)
    
    # 维度分析
    if "dimensions" in result:
        dim_table = Table(title="📊 维度分析", box=box.ROUNDED)
        dim_table.add_column("维度", style="green")
        dim_table.add_column("评分", style="yellow")
        dim_table.add_column("关键点", style="cyan")
        
        for dim in result.get("dimensions", []):
            dim_data = result.get(dim, {})
            score = dim_data.get("score", 0)
            key_points = ", ".join(dim_data.get("key_points", [])[:3])
            
            # 评分颜色
            if score >= 8:
                score_str = f"[green]{score}/10[/]"
            elif score >= 5:
                score_str = f"[yellow]{score}/10[/]"
            else:
                score_str = f"[red]{score}/10[/]"
            
            dim_table.add_row(dim, score_str, key_points or "无")
        
        console.print(dim_table)
    
    # 洞察
    if "insights" in result:
        console.print(Panel(
            "\n".join(result["insights"][:3]),
            title="💡 关键洞察",
            border_style="cyan"
        ))

def _display_analysis_summary(self, results: list, failed_files: list, output_format: OutputFormat):
    """显示分析总结"""
    if not results:
        console.print("[yellow]⚠️ 没有成功的分析结果[/]")
        return
    
    if output_format == OutputFormat.JSON:
        # JSON输出
        print(json.dumps({
            "summary": {
                "total": len(results) + len(failed_files),
                "successful": len(results),
                "failed": len(failed_files)
            },
            "results": results[:10]  # 只输出前10个
        }, ensure_ascii=False, indent=2))
        return
    
    # 终端输出
    console.print("\n" + "="*60)
    console.print("[bold green]📈 分析总结[/]")
    console.print("="*60)
    
    # 统计信息
    stats = Table(show_header=False, box=box.SIMPLE)
    stats.add_column("统计项", style="cyan")
    stats.add_column("数量", style="yellow")
    
    stats.add_row("📁 总文件数", str(len(results) + len(failed_files)))
    stats.add_row("✅ 成功分析", str(len(results)))
    stats.add_row("❌ 分析失败", str(len(failed_files)))
    
    # 类型分布
    type_counts = {}
    for r in results:
        doc_type = r.get("type", "unknown")
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
    
    for doc_type, count in type_counts.items():
        stats.add_row(f"📄 {doc_type}", str(count))
    
    console.print(stats)
    
    # 平均评分
    if results and "dimensions" in results[0]:
        avg_scores = {}
        dims = results[0]["dimensions"]
        
        for dim in dims:
            total = 0
            count = 0
            for r in results:
                if dim in r:
                    total += r[dim].get("score", 0)
                    count += 1
            if count > 0:
                avg_scores[dim] = total / count
        
        if avg_scores:
            score_table = Table(title="🏆 维度平均评分", box=box.ROUNDED)
            score_table.add_column("维度", style="green")
            score_table.add_column("平均分", style="cyan")
            score_table.add_column("水平", style="yellow")
            
            for dim, score in avg_scores.items():
                if score >= 8:
                    level = "优秀 🎯"
                    style = "green"
                elif score >= 6:
                    level = "良好 👍"
                    style = "cyan"
                elif score >= 4:
                    level = "一般 ⚠️"
                    style = "yellow"
                else:
                    level = "需改进 🔧"
                    style = "red"
                
                score_table.add_row(dim, f"{score:.1f}/10", f"[{style}]{level}[/]")
            
            console.print(score_table)
    
    # 失败文件
    if failed_files:
        console.print(Panel(
            "\n".join([f"❌ {f[0]}: {f[1]}" for f in failed_files[:5]]),
            title="⚠️ 失败文件 (前5个)",
            border_style="yellow"
        ))

@app.command()
def evolve(
    iterations: int = typer.Option(3, "--iterations", "-i", help="进化轮数"),
    target: Optional[str] = typer.Option(None, "--target", "-t", 
                                        help="进化目标: performance/accuracy/efficiency"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="试运行，不实际修改"),
    force: bool = typer.Option(False, "--force", "-f", help="强制进化，跳过确认")
):
    """
    执行系统自进化
    继承DNA脚本的自进化循环思想
    """
    show_banner()
    
    if not force:
        console.print("[yellow]⚠️ 警告: 进化将修改系统配置和算法[/]")
        if not Confirm.ask("是否继续?"):
            return
    
    console.print(Panel.fit(
        "[bold cyan]🧬 启动DNA式自进化循环[/]\n\n"
        f"[yellow]迭代次数:[/] {iterations}\n"
        f"[yellow]目标:[/] {target or '综合优化'}\n"
        f"[yellow]模式:[/] {'试运行' if dry_run else '实际执行'}",
        title="进化配置",
        border_style="cyan"
    ))
    
    # 初始化引擎
    analyzer = CogniAnalyzer(name="Coastal Evolution")
    compiler = KnowledgeCompiler(analyzer)
    evo_engine = EvolutionEngine(analyzer, compiler)
    
    # 开始进化循环
    evolution_results = []
    
    for i in range(iterations):
        console.print(f"\n[bold yellow]🔄 第 {i+1}/{iterations} 轮进化[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # 阶段1: 分析当前状态
            progress.add_task("📊 分析系统状态...", total=None)
            status = evo_engine._analyze_knowledge_base()
            
            # 阶段2: 识别改进点
            progress.add_task("🎯 识别优化机会...", total=None)
            improvements = evo_engine._identify_improvements(status, [target] if target else None)
            
            # 阶段3: 执行进化
            if not dry_run:
                progress.add_task("🔧 执行进化...", total=None)
                result = evo_engine._execute_targeted_evolution(improvements)
            else:
                result = {"mode": "dry_run", "improvements": improvements}
            
            # 阶段4: 验证效果
            progress.add_task("✅ 验证进化效果...", total=None)
            if not dry_run:
                validation = evo_engine._validate_evolution(result)
                result["validation"] = validation
            
            evolution_results.append({
                "round": i + 1,
                "timestamp": datetime.now().isoformat(),
                "result": result
            })
            
            console.print(f"[green]✅ 第 {i+1} 轮进化完成[/]")
            
            if i < iterations - 1:
                with console.status("[dim]⏳ 冷却中..."):
                    time.sleep(1)
    
    # 显示进化报告
    _display_evolution_report(evolution_results, dry_run)

def _display_evolution_report(self, results: list, dry_run: bool = False):
    """显示进化报告"""
    console.print("\n" + "="*60)
    console.print("[bold green]📊 进化完成报告[/]")
    console.print("="*60)
    
    for round_result in results:
        round_num = round_result["round"]
        result = round_result["result"]
        
        panel_title = f"第 {round_num} 轮进化"
        if dry_run:
            panel_title += " (试运行)"
        
        improvements = result.get("improvements", [])
        validation = result.get("validation", {})
        
        content = []
     