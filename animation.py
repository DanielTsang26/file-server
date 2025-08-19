import time
from rich.console import Console
from rich.progress import Progress

console = Console()

def boot_animation():
    console.clear()
    console.print(f"\n[cyan] Initializing A.E.G.I.S. AI Interface... [/cyan]\n")

    steps =[
        "[red]* Booting Arc Reactor Core...[/red]",
        "[cyan]* Activating HUD Overlay...[/cyan]",
        "[yellow]* Establishing Data Streams....[/yellow]",
        "[green]* Optimizing System Performance...[/green]",
        "[bold blue]* A.E.G.I.S. Fully Operational.[/bold blue]"
    ]

    with Progress() as progress:
        task = progress.add_task("[cyan]Loading...", total=len(steps))


        for step in steps:
            console.clear()
            progress.update(task, advance=1)
            console.print(step)
            time.sleep(0.8)

    console.print("\n[green]Welcome back, Sir.[/green]\n")

if __name__=="__main__":
    boot_animation()