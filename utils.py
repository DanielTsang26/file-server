import os
import requests
from tqdm import tqdm 
from rich.console import Console


console = Console()
SERVER_URL = "http://127.0.0.1:5000"
UPLOAD_FOLDER = os.path.abspath("uploads")

def upload_file(file_path):
   

    file_path = os.path.abspath(file_path)
    console.print(f"Trying to upload: {file_path}")

    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        console.print(f"[cyan]Uploading {file_name}...[/cyan]")
        
        with open(file_path, 'rb') as file:
            response = requests.post(f"{SERVER_URL}/upload", files={'file': file})

        if response.status_code == 200:
           for _ in tqdm(range(100), desc="Uploading", ascii=" █"):
            pass  # Simulated progress
        console.print("[green]Upload Complete.[/green]")
    else:
        console.print("[red]Error: File not found![/red]")


def download_file(filename):
    console.print(f"[cyan]Downloading {filename}...[/cyan]")
    
    response = requests.get(f"{SERVER_URL}/download/{filename}", stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        for _ in tqdm(range(100), desc="Downloading", ascii=" █"):
            pass  # Simulated progress
        console.print("[green]Download Complete.[/green]")
    else:
        console.print("[red]Error: File not found![/red]")


def list_uploaded_files(): 
    response = requests.get(f"{SERVER_URL}/list_files")

    if response.status_code == 200:
        files = response.json().get("files", [])
        if files:
            console.print("[cyan]Uploaded Files: [/cyan]")
            for file in files:
                console.print(f"- [cyan]{file}[/cyan]")

        else:
            console.print("[yellow]No files uploaded yet.[/yellow]")
    else:
        console.print("[red]Error: Unable to retrieve file list. [/red]") 


def view_file(filename):
    console.print(f"[cyan]fetching content of {filename}...[/cyan]")

    response = requests.get(f"{SERVER_URL}/view/{filename}")


    if response.status_code == 200:
        data = response.json()
        console.print(f"[green]Contents of {filename}: [/green]\n")
        console.print(data["content"])
    else:
        console.print(f"[red]Error: {response.json().get('error', 'Unknown error')}[/red]")