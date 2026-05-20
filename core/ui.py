import time
import sys
import subprocess
import platform
import shutil
from .messages import errors
from .storage import load_data
from .banner_theme import banner_theme
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

console = Console()

class text:
    @staticmethod
    def typing_print(full_text, words_per_chunk=3, delay=0.02) -> str:
        try:
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
        except Exception as e:
            errors.print_error(f"Error on typing_print ({e})", __file__)
    
    @staticmethod
    def get_prompt(ai_model):
        try:
            style = Style.from_dict({
                "blue": "bold ansiblue",
                "red": "bold ansired",
                "white": "bold",
            })
        
            return prompt(
                [
                    ("class:blue", "AI"),
                    ("class:red", "@"),
                    ("class:white", ai_model),
                    ("class:white", "> "),
                ],
                style=style,
                history=FileHistory(".history"),
                auto_suggest=AutoSuggestFromHistory()
            )
        except Exception as e:
            errors.print_error(f"error on get_prompt ({e})", __file__)
    
class look:
    @staticmethod
    def render_banner() -> str:
        try:
            logo = load_data()
            
            themes = banner_theme.available_theme()
            theme_choice = logo['banner_theme']
            
            if theme_choice in themes:
                chosen_theme = themes[theme_choice]
                console.print(chosen_theme())
            else:
                data = load_data()
                errors.print_error(f"Invalid theme name! [Theme: \"[bold]{data['banner_theme']}[/]\"?]\n", __file__)
                
            program_copyright = "Tebac Copyright (C) 2026 nieatmaja\n\tThis program comes with ABSOLUTELY NO WARRANTY.This is\n\tfree software, and you are welcome to redistribute it\n\tunder certain conditions.\n[bold]Please type /help to see available commands![/bold]\nYou can change 'tebac' banner by typing /change-banner <YOUR_PREFERRED_THEME>\n"
                
            console.print(program_copyright)
                
        except Exception as e:
            errors.print_error(e, __file__)
