import time
import sys
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

console = Console()

class text:
    @staticmethod
    def typing_print(full_text, words_per_chunk=3, delay=0.02):
        """
        Streams a string as live-rendered Markdown.
        """
        # Split text into chunks to simulate natural typing
        words = full_text.split(" ")
        current_text = ""
        
        # Initialize the Live display with an empty Markdown object
        with Live(Markdown(""), refresh_per_second=20) as live:
            for i in range(0, len(words), words_per_chunk):
                # Build the text incrementally
                chunk = " ".join(words[i:i+words_per_chunk])
                current_text += ( " " if current_text else "" ) + chunk
                
                # Update the live display with the new Markdown content
                live.update(Markdown(current_text))
                time.sleep(delay)
    
class look:
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