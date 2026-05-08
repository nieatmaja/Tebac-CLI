import sys
import time
import subprocess
import platform
import os
import json
from rich.console import Console
console = Console()

data_file = os.path.abspath("core/data_file.json")

class util:
    @staticmethod
    def if_datafile_not_exists():
        if not os.path.exists(data_file):
            os.makedirs(os.path.dirname(data_file), exist_ok=True)
            
            default_data = {
                "api_key": "<YOUR_API>",
                "site_url": "https://github.com/nieatmaja",
                "site_name": "tebac",
                "model": "<YOUR_PREFFERED_MODEL>"
            }
            
            with open(data_file, 'w') as f:
                json.dump(default_data, f, indent=4)
            
            return default_data

class errors:
    @staticmethod
    def print_error(message) -> str:
        console.print(f"[red]Error occurred: {message}[/red]")

    @staticmethod
    def print_keyboard_interrupt() -> str:
        console.print("\n[red]Interrupted, exiting...[/red]")
        
class look:
    @staticmethod
    def typing_print(text, delay=0.002):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        
    @staticmethod
    def render_banner():
        logo = """
            ███        ▄████████ ▀█████████▄     ▄████████  ▄████████ 
        ▀█████████▄   ███    ███   ███    ███   ███    ███ ███    ███ 
           ▀███▀▀██   ███    █▀    ███    ███   ███    ███ ███    █▀  
            ███   ▀  ▄███▄▄▄      ▄███▄▄▄██▀    ███    ███ ███        
            ███     ▀▀███▀▀▀     ▀▀███▀▀▀██▄  ▀███████████ ███        
            ███       ███    █▄    ███    ██▄   ███    ███ ███    █▄  
            ███       ███    ███   ███    ███   ███    ███ ███    ███ 
           ▄████▀     ██████████ ▄█████████▀    ███    █▀  ████████▀   V.01
        """
    
        print(f"{logo}\n")
        
class basic_commands:
    @staticmethod
    def cls():
        subprocess.run("cls" if platform.system() == "Windows" else "clear")
