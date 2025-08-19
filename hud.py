import time
import psutil
import random
from rich.console import Console
from rich.panel import Panel

console = Console()

def display_hud():
    while True:
        #console.clear()
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        logs = ["Encrypting data...", "Scanning for intrusions...", "Monitoring CPU usage..."]
        log_data = "\n".join(random.sample(logs, k=3))

        panel = Panel.fit(
            f"[bold red]A.E.G.I.S. Private Server[/]\n"
            f"\n[bold cyan]SYSTEM STATUS[/bold cyan]\n"
            f"CPU Usage: [bold red]{cpu_usage}%[/bold red]\n"
            f"Memory Usage: [bold yellow]{memory}%[/bold yellow]\n"
            f"\n[bold yellow]Logs:[/bold yellow]\n[bold blue]{log_data}[/bold blue]\n",
            title="[bold yellow]HUD Interface[/bold yellow]",
            border_style="cyan"
        )

        console.print(panel)
        time.sleep(0.8)


        command = input(">>> ").strip().lower()

        if command =="quit":
            console.print("[bold red]Returning to main menu...[/bold red]")
            break
        else:
            console.print("[bold red]Incorrect command, please enter a valid command...[/bold red]")


       
if __name__=="__main__":
    display_hud()