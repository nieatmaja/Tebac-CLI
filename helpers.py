import sys
import time
import subprocess
import platform
import os
import json
import shlex
from rich.console import Console
console = Console()

data_file = os.path.abspath("core/data_file.json")
PROMPT_FILE = os.path.abspath("core/prompt.txt")
MEMORY_FILE = os.path.abspath("core/memory.json")

## Load configuration data from data_file.json ##
def load_data():
    try:
        util.if_datafile_not_exists()

        if os.path.exists(data_file) and os.path.getsize(data_file) == 0:
            raise json.JSONDecodeError("File is empty", "", 0)

    except Exception as e:
        errors.print_error(e)

    with open(data_file, 'r', encoding="utf-8") as data:
        return json.load(data)

## Load conversation history from memory.json ##    
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

## Save conversation history to memory.json ##
def save_memory(messages):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        errors.print_error(e)

# Clear all saved conversation history in memory.json
def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        console.print(f"[green]Memory cleared![/green]")
    else:
        console.print(f"[yellow]No memory to clear[/yellow]")
    return []

## Function to set API KEY##
def set_api(api_key):
    data_content = load_data()

    data_content['api_key'] = api_key
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)

# Function to set AI MODEL ##
def set_model(model):
    data_content = load_data()

    data_content['model'] = model

    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)
        
def set_site_url(url):
    data_content = load_data()
    
    data_content['site_url'] = url
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)
        
def set_site_name(name):
    data_content = load_data()
    
    data_content['site_name'] = name
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)

## Get AI prompt from prompt.txt ##
def get_prompt():
    if not os.path.exists(PROMPT_FILE):
        default_prompt = "You are tebac, a very helpful and very kind ai that help people anytime."
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(default_prompt)
        return default_prompt
    
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
            else:
                return "You are tebac, a very helpful and very kind ai that help people anytime."
            
    except Exception as e:
        print(f"{colors.red}Failed to read system prompt: {e}{colors.reset}")
        return "You are tebac, a very helpful and very kind ai that help people anytime."

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
        
    @staticmethod
    def check_if_its_command(user_input):
        if user_input in ["exit", "return"]: #exit from the program
            sys.exit(0)
        
        if user_input == "cls": #clear screen
            basic_commands.cls()
            look.render_banner()
            return True
    
        if user_input.startswith("/set-api"): #set api key
            parts = user_input.split(maxsplit=1)

            if len(parts) < 2:
                console.print(f"[yellow]Usage: [/yellow][bold]/set-api <API_KEY>[/bold]")
                return True

            api_key = parts[1].strip()
            set_api(api_key)
            console.print("[bold green]Success![/bold green]")
            return True

        if user_input.startswith("/set-model"): #set ai model
            parts = user_input.split(maxsplit=1)

            if len(parts) < 2:
                console.print(f"[yellow]Usage: [/yellow][bold]/set-model <YOUR_PREFFERED_MODEL>[/bold]")
                return True

            model = parts[1].strip()
            set_model(model)
            console.print("[bold green]Success![/bold green]")
            return True
        
        if user_input.startswith("/set-site-url"):
            parts = user_input.split(maxsplit=1)
            
            if len(parts) < 2:
                console.print(f"[yellow]Usage: [/yellow][bold]/set-site-url <YOUR_SITE_URL>[/bold]")
                return True
            
            url = parts[1].strip()
            set_site_url(url)
            console.print("[bold green]success![/bold green]")
            return True
        
        if user_input.startswith("/set-site-name"):
            parts = user_input.split(maxsplit=1)
            
            if len(parts) < 2:
                console.print(f"[yellow]Usage: [/yellow][bold]/set-site-name <YOUR_SITE_NAME>[/bold]")
                return True
            
            name = parts[1].strip()
            set_site_name(name)
            console.print("[bold green]success![/bold green]")
            return True

        if user_input.startswith("/check-api"): #check api key
            get_data = load_data()
            console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key'][:20]}...")
            return True
    
        if user_input == "/reset": #reset conversation history
            clear_memory()
            return True
        
        if user_input == "/cmd": #run system command
            console.print("Type [bold blue]'exit'/'return'[/bold blue] or [bold purple]CTRL + C[/bold purple] to exit")
            while True:
                try:
                    given_cmd = console.input("[bold yellow]Enter command[/bold yellow]> ")
                
                    if given_cmd in ["return", "exit"]:
                        return True
                
                    cmd_args = shlex.split(given_cmd)
                    if cmd_args:
                        subprocess.run(cmd_args)
                                   
                except Exception as e:
                    errors.print_error(e)
                except KeyboardInterrupt:
                    errors.print_keyboard_interrupt()
                    return True
    
        if user_input == "/help":
            available_command = {
                "basic_command": {
                    "exit/return": "exit from the program",
                    "cls": "clear screen",
                },
                "advanced_command": {
                    "/set-api": "set or change the openrouter api key",
                    "/check-api": "check the api key",
                    "/set-model": "set or change the ai model",
                    "/set-site-url": "set or change program site url",
                    "/set-site-name": "set or change program site name",
                    "/cmd": "run system command directly from the program",
                    "/reset": "reset conversation history",
                },
                "keyboard_shortcut": {
                    "CTRL + C": "Aborting call or exit from the program"
                }
            }
        
            console.print("\n[[bold]Basic command[/bold]]\n")
            for key, value in available_command["basic_command"].items():
                console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]")
            
            print("")
                
            console.print("[[bold]Advanced command[/bold]]\n")
            for key, value in available_command["advanced_command"].items():
                console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]")

            print("")

            console.print("[[bold]Keyboard Shortcut[/bold]]\n")
            for key, value in available_command["keyboard_shortcut"].items():
                console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]")

            print("")
            
            return True
        if user_input == "/cheollima":
            console.print("[bold red]No[/bold red][red] to DPRK![/red]")
            return True

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
        console.print("Tebac Copyright (C) 2026 nieatmaja\n    This program comes with ABSOLUTELY NO WARRANTY.This is\n    free software, and you are welcome to redistribute it\n    under certain conditions.\n[bold]Please type /help to see available commands![/bold]\n")
        
class basic_commands:
    @staticmethod
    def cls():
        subprocess.run("cls" if platform.system() == "Windows" else "clear")
