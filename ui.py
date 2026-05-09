import time
import sys
from rich.console import Console

console = Console()

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
        console.print("Tebac Copyright (C) 2026 nieatmaja\n    This program comes with ABSOLUTELY NO WARRANTY.This is\n    free software, and you are welcome to redistribute it\n    under certain conditions.\n[bold]Please type /help to see available commands![/bold]\n")