"""
Agentic Interactive CLI - Multi-Agent Data Q&A

Premium CLI powered by Rich for beautiful terminal output.
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from loguru import logger
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.columns import Columns
from rich.markdown import Markdown
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich import print as rprint
import time

from config import settings
from utils.data_loader import DataLoader
from agents.agentic_base import AgentContext
from agents.orchestrator import OrchestratorAgent

console = Console()


def print_banner():
    """Display the application banner."""
    console.print(Panel(
        Text("🤖 CORTEX ANALYTICS ENGINE", style="bold cyan") +
        Text("\n\nAgentic Code Engine", style="dim white") +
        Text("\nv3.0 - ELITE TIER", style="dim white"),
        border_style="cyan",
        padding=(1, 2),
        title="[bold white]v3.0[/bold white]",
        subtitle=f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]"
    ))


def print_data_table(data: pd.DataFrame):
    """Display data summary as a table."""
    stats_table = Table(title="📊 Dataset Overview", box=ROUNDED, border_style="cyan")
    stats_table.add_column("Metric", style="cyan", no_wrap=True)
    stats_table.add_column("Value", style="white")
    stats_table.add_row("Total Rows", f"[bold green]{len(data):,}[/bold green]")
    stats_table.add_row("Total Columns", f"[bold blue]{len(data.columns)}[/bold blue]")
    stats_table.add_row("Memory Usage", f"{data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

    cols_table = Table(title="📋 Columns", box=ROUNDED, border_style="blue")
    cols_table.add_column("Name", style="bold cyan")
    cols_table.add_column("Type", style="yellow")
    cols_table.add_column("Unique", style="green")
    cols_table.add_column("Example", style="dim white")

    for col in data.columns[:15]:
        example = str(data[col].iloc[0]) if not data.empty else ""
        cols_table.add_row(
            col,
            str(data[col].dtype),
            str(data[col].nunique()),
            example[:30] + "..." if len(example) > 30 else example
        )
    return stats_table, cols_table


def main():
    """Cortex Analytics Engine v3 Interactive CLI."""
    print_banner()

    console.print("\n")
    console.print(Panel("[bold]📁 DATA LOADING[/bold]", border_style="blue", padding=(0, 2)))

    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        while True:
            rprint("[bold yellow]Enter data file path (CSV, Excel, Parquet):[/bold yellow] ", end="")
            path_input = input().strip().strip('"').strip("'")
            if not path_input:
                continue
            path = Path(path_input)
            if path.exists():
                break
            console.print(f"  [red]✗ File not found:[/red] {path}")

    with console.status("[bold cyan]Loading dataset...", spinner="dots"):
        loader = DataLoader()
        try:
            data = loader.load(str(path))
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]Error loading data:[/bold red] {e}")
            return

    console.print(f"  [green]✓ Loaded[/green] [bold]{path.name}[/bold]")
    stats_table, cols_table = print_data_table(data)
    console.print("\n")
    console.print(stats_table)
    console.print("\n")
    console.print(cols_table)

    console.print("\n")
    console.print(Panel("[bold]🧠 CORTEX ACTIVATION[/bold]", border_style="magenta", padding=(0, 2)))

    with console.status("[bold magenta]Booting Cortex Analytics Engine (v3)...", spinner="dots"):
        context = AgentContext(data)
        cortex = OrchestratorAgent(context)
        time.sleep(0.8)

    console.print("\n  [green]✓ Cortex Analytics Engine v3 Online.[/green] Multi-Agent Council Ready.")

    console.print("\n")
    console.print(Panel("[bold]💬 CORTEX ANALYSIS[/bold]", border_style="green", padding=(0, 2)))
    console.print("\n  [dim]Commands: [cyan]quit[/cyan] to exit, [cyan]clear[/cyan] to clear screen[/dim]")

    while True:
        console.print("\n" + "─" * 80, style="dim")
        try:
            question = Prompt.ask("  [bold cyan]❯[/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n\n  [cyan]Session ended. Goodbye! 👋[/cyan]\n")
            break

        if not question.strip():
            continue

        if question.lower() in ['quit', 'exit', 'q']:
            console.print("\n  [cyan]Session ended. Goodbye! 👋[/cyan]\n")
            break

        if question.lower() == 'clear':
            console.clear()
            continue

        try:
            start_time = time.time()
            with console.status("[bold magenta]Cortex Thinking & Coding...[/bold magenta]", spinner="dots"):
                result = cortex.run(question)

            elapsed = time.time() - start_time
            panel = Panel(
                Text(str(result.result), style="white"),
                title="[bold green]💡 Insight[/bold green]",
                subtitle=f"[dim]Time: {elapsed:.2f}s | Confidence: {result.confidence*100:.0f}%[/dim]",
                border_style="green",
                padding=(1, 2)
            )
            console.print(panel)

            if result.metadata.get("code"):
                pass

        except Exception as e:
            console.print(f"[bold red]System Error:[/bold red] {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
