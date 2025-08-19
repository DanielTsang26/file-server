from cli import start_cli
from server import run_server
from threading import Thread




def main():
    #Starts the server in a separate thread
    server_thread = Thread(target=run_server)
    server_thread.start()

    
    
    start_cli()

if __name__ =="__main__":
    main()

