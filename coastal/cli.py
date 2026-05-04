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
        
        if improvements:
            content.append("[yellow]🎯 改进点:[/]")
            for imp in improvements[:5]:  # 只显示前5个
                content.append(f"  • {imp}")
            if len(improvements) > 5:
                content.append(f"  ... 等 {len(improvements)} 个改进点")
        
        if validation:
            content.append("\n[green]✅ 验证结果:[/]")
            for key, value in validation.items():
                if isinstance(value, (int, float)):
                    content.append(f"  {key}: {value:.2%}")
                else:
                    content.append(f"  {key}: {value}")
        
        if not content:
            content.append("[dim]无详细改进信息[/]")
        
        console.print(Panel(
            "\n".join(content),
            title=panel_title,
            border_style="cyan" if not dry_run else "dim"
        ))
    
    # 总体统计
    if not dry_run and results:
        final_result = results[-1]["result"]
        final_validation = final_result.get("validation", {})
        
        if final_validation:
            stats_table = Table(title="📈 进化效果统计", box=box.ROUNDED)
            stats_table.add_column("指标", style="cyan")
            stats_table.add_column("进化前", style="dim")
            stats_table.add_column("进化后", style="green")
            stats_table.add_column("提升", style="yellow")
            
            # 这里可以添加具体的统计数据
            # 例如: 分析速度、准确率、覆盖率等
            
            console.print(stats_table)
    
    console.print(f"\n[bold green]🎉 进化完成! 共执行 {len(results)} 轮进化{' (试运行)' if dry_run else ''}[/]")
    
    # 保存报告
    if not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = Path("evolution_reports") / f"evolution_{timestamp}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "total_rounds": len(results),
                    "completed_at": timestamp,
                    "mode": "full" if not dry_run else "dry_run"
                },
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]📁 进化报告已保存: {report_file}[/]")

@app.command()
def self_analyze(
    detail: bool = typer.Option(False, "--detail", "-d", help="显示详细分析"),
    export: Optional[Path] = typer.Option(None, "--export", "-e", help="导出分析结果")
):
    """
    系统自我分析 - 继承DNA脚本的自指特性
    """
    show_banner()
    
    console.print("[bold cyan]🔍 启动自指分析...[/]")
    console.print("[dim]系统正在分析自身的代码和配置...[/]\n")
    
    # 创建分析器
    analyzer = CogniAnalyzer(name="Coastal Console")
    
    with console.status("[bold cyan]分析中...") as status:
        # 1. 分析系统代码
        status.update("[bold cyan]分析代码结构...")
        code_analysis = self._analyze_system_code()
        
        # 2. 分析配置文件
        status.update("[bold cyan]分析配置...")
        config_analysis = self._analyze_configurations()
        
        # 3. 分析知识库状态
        status.update("[bold cyan]分析知识库...")
        knowledge_analysis = analyzer.analyze_content("", "系统设计")
        
        # 4. 生成综合报告
        status.update("[bold cyan]生成报告...")
        report = self._generate_self_analysis_report(
            code_analysis, 
            config_analysis, 
            knowledge_analysis
        )
    
    # 显示分析结果
    self._display_self_analysis(report, detail)
    
    # 导出结果
    if export:
        with open(export, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        console.print(f"[green]📁 自指分析已导出: {export}[/]")
    
    # 显示改进建议
    if "suggestions" in report:
        console.print("\n[bold yellow]💡 改进建议:[/]")
        for i, suggestion in enumerate(report["suggestions"][:5], 1):
            console.print(f"  {i}. {suggestion}")

def _analyze_system_code(self) -> dict:
    """分析系统代码"""
    # 获取项目文件结构
    project_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".json", ".md", ".txt")):
                rel_path = os.path.join(root, file)
                project_files.append({
                    "path": rel_path,
                    "size": os.path.getsize(rel_path),
                    "type": "python" if file.endswith(".py") else "other"
                })
    
    # 计算代码统计
    code_stats = {
        "total_files": len(project_files),
        "python_files": len([f for f in project_files if f["type"] == "python"]),
        "total_lines": 0,
        "total_size": sum(f["size"] for f in project_files),
        "file_structure": self._analyze_directory_structure(".")
    }
    
    return code_stats

def _analyze_configurations(self) -> dict:
    """分析配置文件"""
    config_files = [
        "coastal.config.json",
        "pyproject.toml",
        "requirements.txt",
        ".env",
        "config.yaml"
    ]
    
    configs = {}
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    content = f.read()
                configs[config_file] = {
                    "exists": True,
                    "size": len(content),
                    "lines": content.count("\n") + 1
                }
            except:
                configs[config_file] = {"exists": True, "error": "无法读取"}
        else:
            configs[config_file] = {"exists": False}
    
    return configs

def _generate_self_analysis_report(self, code_analysis: dict, 
                                  config_analysis: dict, 
                                  knowledge_analysis: dict) -> dict:
    """生成自我分析报告"""
    report = {
        "metadata": {
            "analyzed_at": datetime.now().isoformat(),
            "system": "Coastal Console",
            "version": VERSION
        },
        "code_analysis": code_analysis,
        "config_analysis": config_analysis,
        "knowledge_analysis": knowledge_analysis,
        "health_score": self._calculate_health_score(code_analysis, config_analysis),
        "suggestions": self._generate_improvement_suggestions(code_analysis, config_analysis)
    }
    
    return report

def _display_self_analysis(self, report: dict, detail: bool = False):
    """显示自我分析结果"""
    console.print("\n" + "="*60)
    console.print("[bold green]🧬 自指分析报告[/]")
    console.print("="*60)
    
    # 系统信息
    metadata = report["metadata"]
    info_table = Table(show_header=False, box=box.SIMPLE)
    info_table.add_column("属性", style="cyan")
    info_table.add_column("值", style="white")
    
    info_table.add_row("系统名称", metadata["system"])
    info_table.add_row("版本", metadata["version"])
    info_table.add_row("分析时间", metadata["analyzed_at"])
    info_table.add_row("健康度", f"{report['health_score']}/100")
    
    console.print(info_table)
    
    # 代码分析
    code_stats = report["code_analysis"]
    code_table = Table(title="📁 代码结构分析", box=box.ROUNDED)
    code_table.add_column("指标", style="cyan")
    code_table.add_column("值", style="yellow")
    code_table.add_column("状态", style="green")
    
    code_table.add_row("总文件数", str(code_stats["total_files"]), 
                       "✅" if code_stats["total_files"] > 0 else "❌")
    code_table.add_row("Python文件数", str(code_stats["python_files"]), 
                       "✅" if code_stats["python_files"] > 0 else "⚠️")
    code_table.add_row("总大小", f"{code_stats['total_size'] / 1024:.1f} KB", 
                       "✅" if code_stats["total_size"] < 1024*100 else "⚠️")
    
    console.print(code_table)
    
    if detail and "file_structure" in code_stats:
        # 显示文件结构
        file_tree = Tree("📁 项目结构")
        self._build_structure_tree(file_tree, code_stats["file_structure"])
        console.print(file_tree)
    
    # 配置分析
    configs = report["config_analysis"]
    config_table = Table(title="⚙️ 配置分析", box=box.ROUNDED)
    config_table.add_column("配置文件", style="cyan")
    config_table.add_column("状态", style="yellow")
    config_table.add_column("详情", style="dim")
    
    for config_file, info in configs.items():
        if info.get("exists"):
            status = "✅ 存在"
            details = f"{info.get('lines', '?')} 行, {info.get('size', '?')} 字节"
        else:
            status = "❌ 缺失"
            details = "建议创建"
        
        config_table.add_row(config_file, status, details)
    
    console.print(config_table)
    
    # 知识库分析
    if "knowledge_analysis" in report and report["knowledge_analysis"]:
        knowledge = report["knowledge_analysis"]
        if "dimensions" in knowledge:
            k_table = Table(title="📊 知识库分析", box=box.ROUNDED)
            k_table.add_column("维度", style="cyan")
            k_table.add_column("评分", style="yellow")
            
            for dim in knowledge.get("dimensions", []):
                if dim in knowledge:
                    score = knowledge[dim].get("score", 0)
                    score_str = f"{score}/10"
                    if score >= 8:
                        score_str = f"[green]{score_str}[/]"
                    elif score >= 5:
                        score_str = f"[yellow]{score_str}[/]"
                    else:
                        score_str = f"[red]{score_str}[/]"
                    
                    k_table.add_row(dim, score_str)
            
            console.print(k_table)

@app.command()
def compile(
    source: Path = typer.Argument(..., help="源文件或目录"),
    output: Path = typer.Option(Path("output"), "--output", "-o", 
                               help="输出目录"),
    format: OutputFormat = typer.Option(OutputFormat.MARKDOWN, "--format", "-f", 
                                        help="输出格式"),
    minify: bool = typer.Option(False, "--minify", "-m", help="最小化输出"),
    compress: bool = typer.Option(False, "--compress", "-c", help="压缩输出")
):
    """
    编译知识库
    """
    show_banner()
    
    if not source.exists():
        console.print(f"[red]❌ 源路径不存在: {source}[/]")
        return
    
    output.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]🔧 编译: {source} → {output} ({format.value})[/]")
    
    # 初始化编译器和分析器
    analyzer = CogniAnalyzer()
    compiler = KnowledgeCompiler(analyzer)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        # 收集源文件
        progress.add_task("📁 收集源文件...", total=None)
        source_files = self._collect_source_files(source)
        
        if not source_files:
            console.print("[yellow]⚠️ 没有找到可编译的文件[/]")
            return
        
        console.print(f"[cyan]找到 {len(source_files)} 个源文件[/]")
        
        compiled_count = 0
        failed_files = []
        
        compile_task = progress.add_task("🔨 编译中...", total=len(source_files))
        
        for file_path in source_files:
            try:
                # 分析文件
                content = file_path.read_text(encoding="utf-8")
                analysis = analyzer.analyze_content(content)
                
                # 编译为schema
                schema = compiler.compile_to_schema(analysis)
                
                # 根据格式输出
                if format == OutputFormat.MARKDOWN:
                    output_content = compiler.compile_to_wiki(schema)
                    output_file = output / f"{file_path.stem}.md"
                elif format == OutputFormat.JSON:
                    output_content = json.dumps(schema, indent=2, ensure_ascii=False)
                    output_file = output / f"{file_path.stem}.json"
                elif format == OutputFormat.HTML:
                    output_content = self._convert_to_html(schema)
                    output_file = output / f"{file_path.stem}.html"
                else:
                    output_content = json.dumps(schema, ensure_ascii=False)
                    output_file = output / f"{file_path.stem}.txt"
                
                # 写入输出
                output_file.write_text(output_content, encoding="utf-8")
                compiled_count += 1
                
            except Exception as e:
                failed_files.append((file_path.name, str(e)))
                logger.log(f"编译失败: {file_path} - {e}", LogLevel.ERROR, "Compile")
            
            progress.advance(compile_task)
    
    # 显示结果
    self._display_compile_summary(compiled_count, len(source_files), output, failed_files)

def _display_compile_summary(self, compiled: int, total: int, output_dir: Path, 
                            failed_files: list):
    """显示编译总结"""
    console.print("\n" + "="*60)
    console.print("[bold green]📦 编译完成[/]")
    console.print("="*60)
    
    summary_table = Table(show_header=False, box=box.ROUNDED)
    summary_table.add_column("项目", style="cyan")
    summary_table.add_column("值", style="yellow")
    
    summary_table.add_row("📁 总文件数", str(total))
    summary_table.add_row("✅ 成功编译", str(compiled))
    summary_table.add_row("❌ 编译失败", str(len(failed_files)))
    summary_table.add_row("📂 输出目录", str(output_dir.absolute()))
    summary_table.add_row("🎯 成功率", f"{(compiled/total*100):.1f}%" if total > 0 else "0%")
    
    console.print(summary_table)
    
    if failed_files:
        console.print(Panel(
            "\n".join([f"❌ {name}: {error}" for name, error in failed_files[:3]]),
            title="⚠️ 失败文件 (前3个)",
            border_style="yellow"
        ))
        if len(failed_files) > 3:
            console.print(f"[dim]... 还有 {len(failed_files)-3} 个失败文件[/]")
    
    console.print(f"\n[green]🎉 编译完成! 查看输出: {output_dir.absolute()}[/]")

@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="端口号"),
    host: str = typer.Option("localhost", "--host", "-h", help="主机地址"),
    theme: Theme = typer.Option(Theme.OCEAN, "--theme", "-t", help="界面主题"),
    watch: bool = typer.Option(False, "--watch", "-w", help="监视文件变化"),
    api_only: bool = typer.Option(False, "--api-only", "-a", help="仅启动API")
):
    """
    启动本地服务
    """
    show_banner()
    
    console.print(f"[cyan]🌐 启动服务: http://{host}:{port}[/]")
    console.print(f"[dim]主题: {theme.value} | 监视: {watch} | API模式: {api_only}[/]\n")
    
    # 检查依赖
    try:
        import uvicorn
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse, JSONResponse
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
    except ImportError:
        console.print("[yellow]⚠️ 缺少Web依赖，正在安装...[/]")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "fastapi", "uvicorn", "jinja2"])
            console.print("[green]✅ 依赖安装完成[/]")
            import uvicorn
            from fastapi import FastAPI, Request
        except:
            console.print("[red]❌ 安装依赖失败，请手动安装: pip install fastapi uvicorn jinja2[/]")
            return
    
    # 创建应用
    app_title = f"Coastal Console - 知识引擎 (v{VERSION})"
    fastapi_app = FastAPI(title=app_title, version=VERSION)
    
    # 创建必要的目录
    static_dir = Path("static")
    templates_dir = Path("templates")
    static_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)
    
    # 创建默认模板
    self._create_web_templates(templates_dir, theme)
    
    # 挂载静态文件
    fastapi_app.mount("/static", StaticFiles(directory=static_dir), name="static")
    templates = Jinja2Templates(directory=str(templates_dir))
    
    # API路由
    @fastapi_app.get("/")
    async def root(request: Request):
        """首页"""
        if api_only:
            return JSONResponse({
                "service": "Coastal Console API",
                "version": VERSION,
                "endpoints": [
                    "/api/status",
                    "/api/knowledge",
                    "/api/analyze",
                    "/api/evolve"
                ]
            })
        return templates.TemplateResponse("index.html", {"request": request})
    
    @fastapi_app.get("/api/status")
    async def get_status():
        """获取状态"""
        analyzer = CogniAnalyzer()
        return {
            "status": "running",
            "version": VERSION,
            "system": analyzer.name,
            "analysis_count": len(analyzer.analysis_history),
            "evolution_count": analyzer.evolution_count,
            "uptime": time.time()  # 简化版本
        }
    
    @fastapi_app.post("/api/analyze")
    async def analyze_text(text: str, content_type: str = "auto"):
        """分析文本"""
        analyzer = CogniAnalyzer()
        result = analyzer.analyze_content(text, content_type)
        return result
    
    @fastapi_app.get("/api/knowledge")
    async def get_knowledge():
        """获取知识库"""
        # 这里可以返回知识库内容
        return {"knowledge": "正在开发中..."}
    
    console.print("[green]✅ FastAPI应用已创建[/]")
    console.print("[yellow]👉 按 Ctrl+C 停止服务[/]\n")
    
    # 启动服务
    try:
        config = uvicorn.Config(
            fastapi_app,
            host=host,
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 服务已停止[/]")
    except Exception as e:
        console.print(f"[red]❌ 服务启动失败: {e}[/]")

@app.command()
def status():
    """
    显示系统状态
    """
    show_banner()
    show_status()
    
    # 检查系统健康状态
    health = self._check_system_health()
    
    if health["all_ok"]:
        console.print(Panel.fit(
            "[green]✅ 所有系统正常[/]",
            title="系统健康",
            border_style="green"
        ))
    else:
        issues = [issue for issue, ok in health.items() if not ok and issue != "all_ok"]
        console.print(Panel.fit(
            "\n".join([f"[yellow]⚠️ {issue}[/]" for issue in issues]),
            title="系统警告",
            border_style="yellow"
        ))

@app.command()
def config(
    key: Optional[str] = typer.Argument(None, help="配置键"),
    value: Optional[str] = typer.Argument(None, help="配置值"),
    list_all: bool = typer.Option(False, "--list", "-l", help="列出所有配置"),
    get: bool = typer.Option(False, "--get", "-g", help="获取配置值"),
    set: bool = typer.Option(False, "--set", "-s", help="设置配置值")
):
    """
    管理系统配置
    """
    config_file = Path("coastal.config.json")
    
    if not config_file.exists():
        console.print("[red]❌ 配置文件不存在，请先运行 init[/]")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    if list_all:
        # 列出所有配置
        console.print("[bold cyan]📋 当前配置:[/]")
        self._display_config(config)
    elif get and key:
        # 获取单个配置
        value = self._get_config_value(config, key.split("."))
        if value is not None:
            console.print(f"[cyan]{key}:[/] {value}")
        else:
            console.print(f"[red]❌ 配置不存在: {key}[/]")
    elif set and key and value is not None:
        # 设置配置
        try:
            # 尝试解析值
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            
            self._set_config_value(config, key.split("."), value)
            
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✅ 配置已更新: {key} = {value}[/]")
        except Exception as e:
            console.print(f"[red]❌ 设置失败: {e}[/]")
    else:
        # 显示帮助
        console.print("[yellow]📖 配置管理用法:[/]")
        console.print("  coastal config --list                  # 列出所有配置")
        console.print("  coastal config --get <key>             # 获取配置值")
        console.print("  coastal config --set <key> <value>     # 设置配置值")
        console.print("  coastal config                          # 显示此帮助")

def _display_config(self, config: dict, prefix: str = ""):
    """递归显示配置"""
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            console.print(f"[cyan]{full_key}[/]:")
            self._display_config(value, full_key)
        elif isinstance(value, list):
            console.print(f"[cyan]{full_key}[/]:")
            for i, item in enumerate(value[:5]):  # 只显示前5个
                console.print(f"  [{i}] {item}")
            if len(value) > 5:
                console.print(f"  ... 等 {len(value)} 个项目")
        else:
            if isinstance(value, bool):
                value_str = f"[green]{value}[/]" if value else f"[red]{value}[/]"
            elif isinstance(value, (int, float)):
                value_str = f"[yellow]{value}[/]"
            else:
                value_str = f"[white]{value}[/]"
            
            console.print(f"  [cyan]{full_key}[/]: {value_str}")

def _get_config_value(self, config: dict, keys: list):
    """递归获取配置值"""
    if not keys:
        return config
    
    key = keys[0]
    if key in config:
        return self._get_config_value(config[key], keys[1:])
    return None

def _set_config_value(self, config: dict, keys: list, value):
    """递归设置配置值"""
    if len(keys) == 1:
        config[keys[0]] = value
    else:
        if keys[0] not in config:
            config[keys[0]] = {}
        self._set_config_value(config[keys[0]], keys[1:], value)

def _check_system_health(self) -> dict:
    """检查系统健康状态"""
    health = {
        "all_ok": True
    }
    
    # 检查必要目录
    required_dirs = ["sources", "schema", "wiki"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            health[f"dir_{dir_name}"] = True
        else:
            health[f"dir_{dir_name}"] = False
            health["all_ok"] = False
    
    # 检查配置文件
    config_file = Path("coastal.config.json")
    if config_file.exists():
        health["config_file"] = True
        try:
            with open(config_file, "r") as f:
                json.load(f)
            health["config_valid"] = True
        except:
            health["config_valid"] = False
            health["all_ok"] = False
    else:
        health["config_file"] = False
        health["config_valid"] = False
        health["all_ok"] = False
    
    # 检查源文件
    source_files = list(Path("sources").glob("*"))
    if source_files:
        health["has_sources"] = True
    else:
        health["has_sources"] = False
        # 这不一定是个错误，只是警告
        health["all_ok"] = False
    
    return health

def _create_web_templates(self, templates_dir: Path, theme: Theme):
    """创建Web模板"""
    # 创建主题CSS
    theme_colors = {
        "dark": {
            "bg": "#1a1a1a",
            "text": "#ffffff",
            "primary": "#0ea5e9",
            "secondary": "#3b82f6"
        },
        "light": {
            "bg": "#ffffff",
            "text": "#1a1a1a",
            "primary": "#2563eb",
            "secondary": "#3b82f6"
        },
        "ocean": {
            "bg": "#0f172a",
            "text": "#e2e8f0",
            "primary": "#0ea5e9",
            "secondary": "#06b6d4"
        },
        "forest": {
            "bg": "#0f172a",
            "text": "#d1fae5",
            "primary": "#10b981",
            "secondary": "#059669"
        }
    }
    
    colors = theme_colors[theme.value]
    
    # 创建CSS文件
    css_content = f"""
:root {{
    --bg-color: {colors['bg']};
    --text-color: {colors['text']};
    --primary-color: {colors['primary']};
    --secondary-color: {colors['secondary']};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}}

.header {{
    text-align: center;
    padding: 2rem 0;
    border-bottom: 2px solid var(--primary-color);
    margin-bottom: 2rem;
}}

.header h1 {{
    color: var(--primary-color);
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header .subtitle {{
    color: var(--secondary-color);
    opacity: 0.8;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}}

.stat-card {{
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
}}

.stat-card h3 {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
    opacity: 0.7;
}}

.stat-card .value {{
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary-color);
}}

.content {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
}}

@media (max-width: 768px) {{
    .content {{
        grid-template-columns: 1fr;
    }}
}}

.main-content {{
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 8px;
}}

.sidebar {{
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 8px;
}}

.btn {{
    display: inline-block;
    background: var(--primary-color);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: opacity 0.3s;
}}

.btn:hover {{
    opacity: 0.9;
}}

.btn-secondary {{
    background: var(--secondary-color);
}}
"""
    
    (templates_dir / "static" / "css").mkdir(parents=True, exist_ok=True)
    (templates_dir / "static" / "css" / "style.css").write_text(css_content, encoding="utf-8")
    
    # 创建HTML模板
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-water"></i> Coastal Console</h1>
            <p class="subtitle">基于DNA四维分析思想的智能知识引擎</p>
        </header>
        
        <div class="stats-grid" id="stats">
            <div class="stat-card">
                <h3><i class="fas fa-file-alt"></i> 知识文档</h3>
                <div class="value" id="doc-count">0</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-brain"></i> 分析次数</h3>
                <div class="value" id="analysis-count">0</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-code-branch"></i> 进化轮数</h3>
                <div class="value" id="evolution-count">0</div>
            </div>
            <div class="stat-card">
                <h3><i class="fas fa-project-diagram"></i> 关联数量</h3>
                <div class="value" id="connection-count">0</div>
            </div>
        </div>
        
        <div class="content">
            <main class="main-content">
                <h2><i class="fas fa-tachometer-alt"></i> 控制面板</h2>
                
                <div style="margin: 1.5rem 0;">
                    <button class="btn" onclick="analyzeText()">
                        <i class="fas fa-search"></i> 快速分析
                    </button>
                    <button class="btn btn-secondary" onclick="viewKnowledge()">
                        <i class="fas fa-book"></i> 查看知识库
                    </button>
                    <button class="btn" onclick="startEvolution()">
                        <i class="fas fa-sync-alt"></i> 开始进化
                    </button>
                </div>
                
                <div id="analysis-result" style="margin-top: 2rem;"></div>
                
                <h3 style="margin-top: 2rem;"><i class="fas fa-history"></i> 最近活动</h3>
                <div id="recent-activity"></div>
            </main>
            
            <aside class="sidebar">
                <h3><i class="fas fa-info-circle"></i> 系统信息</h3>
                <div id="system-info"></div>
                
                <h3 style="margin-top: 2rem;"><i class="fas fa-bolt"></i> 快速操作</h3>
                <div style="margin-top: 1rem;">
                    <button class="btn" style="width: 100%; margin-bottom: 0.5rem;" onclick="uploadDocument()">
                        <i class="fas fa-upload"></i> 上传文档
                    </button>
                    <button class="btn btn-secondary" style="width: 100%; margin-bottom: 0.5rem;" onclick="selfAnalyze()">
                        <i class="fas fa-eye"></i> 自我分析
                    </button>
                    <button class="btn" style="width: 100%;" onclick="exportData()">
                        <i class="fas fa-download"></i> 导出数据
                    </button>
                </div>
                
                <h3 style="margin-top: 2rem;"><i class="fas fa-question-circle"></i> 帮助</h3>
                <p style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;">
                    使用 <code>coastal --help</code> 查看所有命令<br>
                    查看文档: <a href="#" style="color: var(--primary-color);">https://coastal.example.com</a>
                </p>
            </aside>
        </div>
    </div>
    
    <script>
        // 加载系统状态
        async function loadSystemStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('doc-count').textContent = '...';
                document.getElementById('analysis-count').textContent = data.analysis_count || 0;
                document.getElementById('evolution-count').textContent = data.evolution_count || 0;
                document.getElementById('connection-count').textContent = '...';
                
                // 显示系统信息
                const systemInfo = document.getElementById('system-info');
                systemInfo.innerHTML = `
                    <p><strong>版本:</strong> ${data.version || '1.0.0'}</p>
                    <p><strong>状态:</strong> <span style="color: #10b981;">● 运行中</span></p>
                    <p><strong>服务:</strong> ${data.system || 'Coastal Console'}</p>
                `;
                
            } catch (error) {
                console.error('加载状态失败:', error);
            }
        }
        
        // 分析文本
        async function analyzeText() {
            const text = prompt('请输入要分析的文本:', '');
            if (!text) return;
            
            const resultDiv = document.getElementById('analysis-result');
            resultDiv.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> 分析中...</p>';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text, content_type: 'auto' })
                });
                
                const data = await response.json();
                
                resultDiv.innerHTML = `
                    <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">
                        <h4><i class="fas fa-chart-bar"></i> 分析结果</h4>
                        <p><strong>类型:</strong> ${data.type || '未知'}</p>
                        <p><strong>深度:</strong> ${data.depth || 0}</p>
                        <p><strong>时间:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
                    </div>
                `;
                
            } catch (error) {
                resultDiv.innerHTML = '<p style="color: #ef4444;">分析失败</p>';
            }
        }
        
        // 加载页面时初始化
        document.addEventListener('DOMContentLoaded', loadSystemStatus);
        
        // 其他函数占位
        function viewKnowledge() { alert('知识库功能开发中...'); }
        function startEvolution() { alert('进化功能开发中...'); }
        function uploadDocument() { alert('上传功能开发中...'); }
        function selfAnalyze() { alert('自我分析功能开发中...'); }
        function exportData() { alert('导出功能开发中...'); }
    </script>
</body>
</html>
"""
    
    (templates_dir / "index.html").write_text(html_content, encoding="utf-8")

@app.command()
def docs(
    command: Optional[str] = typer.Argument(None, help="命令名称"),
    web: bool = typer.Option(False, "--web", "-w", help="在浏览器中打开文档"),
    markdown: bool = typer.Option(False, "--markdown", "-m", help="输出Markdown格式")
):
    """
    查看文档
    """
    if web:
        # 在浏览器中打开文档
        import webbrowser
        webbrowser.open("https://coastal.example.com/docs")
        return
    
    commands_docs = {
        "init": {
            "description": "初始化新的知识库项目",
            "usage": "coastal init <project_name> [--template TEMPLATE] [--force]",
            "options": {
                "--template, -t": "模板类型: default/research/engineering",
                "--force, -f": "强制覆盖已存在项目"
            },
            "example": "coastal init my-project --template research"
        },
        "analyze": {
            "description": "分析文档并提取知识",
            "usage": "coastal analyze <path> [--type TYPE] [--recursive] [--format FORMAT] [--verbose]",
            "options": {
                "--type, -t": "内容类型: tech/paper/business/note/auto",
                "--recursive, -r": "递归分析子目录",
                "--format, -f": "输出格式: json/markdown/terminal/html/pdf",
                "--verbose, -v": "详细输出"
            },
            "example": "coastal analyze ./docs --type tech --format json"
        },
        "evolve": {
            "description": "执行系统自进化",
            "usage": "coastal evolve [--iterations ITERATIONS] [--target TARGET] [--dry-run] [--force]",
            "options": {
                "--iterations, -i": "进化轮数 (默认: 3)",
                "--target, -t": "进化目标: performance/accuracy/efficiency",
                "--dry-run, -d": "试运行，不实际修改",
                "--force, -f": "强制进化，跳过确认"
            },
            "example": "coastal evolve --iterations 5 --target performance"
        },
        "compile": {
            "description": "编译知识库",
            "usage": "coastal compile <source> [--output OUTPUT] [--format FORMAT] [--minify] [--compress]",
            "options": {
                "--output, -o": "输出目录 (默认: ./output)",
                "--format, -f": "输出格式: json/markdown/terminal/html/pdf",
                "--minify, -m": "最小化输出",
                "--compress, -c": "压缩输出"
            },
            "example": "coastal compile ./sources --output ./wiki --format markdown"
        },
        "serve": {
            "description": "启动本地Web服务",
            "usage": "coastal serve [--port PORT] [--host HOST] [--theme THEME] [--watch] [--api-only]",
            "options": {
                "--port, -p": "端口号 (默认: 8000)",
                "--host, -h": "主机地址 (默认: localhost)",
                "--theme, -t": "界面主题: dark/light/ocean/forest",
                "--watch, -w": "监视文件变化",
                "--api-only, -a": "仅启动API，不提供Web界面"
            },
            "example": "coastal serve --port 8080 --theme ocean"
        },
        "self-analyze": {
            "description": "系统自我分析",
            "usage": "coastal self-analyze [--detail] [--export EXPORT]",
            "options": {
                "--detail, -d": "显示详细分析结果",
                "--export, -e": "导出分析结果到文件"
            },
            "example": "coastal self-analyze --detail --export analysis.json"
        },
        "status": {
            "description": "显示系统状态",
            "usage": "coastal status",
            "example": "coastal status"
        },
        "config": {
            "description": "管理系统配置",
            "usage": "coastal config [COMMAND] [OPTIONS]",
            "subcommands": {
                "--list, -l": "列出所有配置",
                "--get, -g <key>": "获取配置值",
                "--set, -s <key> <value>": "设置配置值"
            },
            "example": "coastal config --get system.theme"
        },
        "docs": {
            "description": "查看文档",
            "usage": "coastal docs [COMMAND] [--web] [--markdown]",
            "options": {
                "--web, -w": "在浏览器中打开文档",
                "--markdown, -m": "输出Markdown格式"
            },
            "example": "coastal docs analyze"
        }
    }
    
    if command:
        # 显示特定命令的文档
        if command in commands_docs:
            doc = commands_docs[command]
            
            if markdown:
                # Markdown格式
                print(f"# `coastal {command}`\n")
                print(f"**{doc['description']}**\n")
                print(f"## 使用方法\n```bash\n{doc['usage']}\n```\n")
                
                if "options" in doc and doc["options"]:
                    print("## 选项\n")
                    for opt, desc in doc["options"].items():
                        print(f"- `{opt}`: {desc}")
                    print()
                
                if "example" in doc:
                    print(f"## 示例\n```
