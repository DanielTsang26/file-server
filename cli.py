import atexit
import requests
from utils import list_uploaded_files
from animation import boot_animation
from hud import display_hud
from utils import upload_file, download_file
from rich.console import Console
from server import run_server
from threading import Thread
from utils import view_file
import time

console = Console()
server_thread = None
SERVER_URL = "http://127.0.0.1:5000"
#data = {"username": "admin", 
       # "password": "181290"}
token = None

def stop_server():
    try:
        requests.post("http://127.0.0.1:5000/shutdown")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error shutting down server: {e}[/red]")


def start_cli():
    boot_animation()
    console.print("[bold green]A.E.G.I.S. ")

   # global server_thread  
    #server_thread = Thread(target=run_server)
    #server_thread.start()


    atexit.register(stop_server)


    while True:
        console.print("\n[bold red]Awaiting Command ...[/bold red] ([green]Type 'help' for commands[/green])")
        command = input(">>> ").strip().lower()

        if command == "help":
            console.print("""
            [cyan]Available Commands:[/cyan]
            [bold yellow]upload <file_path>[/bold yellow]   - Upload a file to the server.
            [bold yellow]download <filename>[/bold yellow]  - Download a file from the server.
            [bold yellow]view <file_path>[/bold yellow]      - View the contents of an uploaded file.               
            [bold yellow]list[/bold yellow]                 - Show the list of files uploaded to server.             
            [bold yellow]status[/bold yellow]               - Show live system stats.
            [bold yellow]exit[/bold yellow]                 - Shut down the server.
            """)

        elif command.startswith("upload"):
            file_path = command.split(" ", 1)[1]
            upload_file(file_path)

        elif command.startswith("download "):
            filename= command.split(" ", 1)[1]
            download_file(filename)

        elif command == "status":
            display_hud()
        
        elif command.startswith("view "):
            filename = command.split(" ", 1)[1]
            view_file(filename)
        
        elif command == "list":
            files = list_uploaded_files()
            if files:
                console.print("[bold green]Uploaded Files:[/bold green]")
                for file in files:
                    console.print(f" - {file}")
                else:
                    console.print("[bold yellow]No files uploaded yet. [/bold yellow]")

        elif command == "exit":
            console.print("[bold red] Shutting down A.E.G.I.S. system ...[/bold red]")
            stop_server()
        else:
            console.print("[red]Invalid command! Type help for options.[/red]")

if __name__=="__main__":
    start_cli()

