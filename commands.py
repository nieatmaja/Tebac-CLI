import json
import shlex
import subprocess
import sys
import platform
from errors import errors
from ui import look
from set_config import set_api, set_model, set_site_name, set_site_url
from rich.console import Console

console = Console()
        
class basic_commands:
    @staticmethod
    def cls():
        subprocess.run("cls" if platform.system() == "Windows" else "clear")

class util:
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