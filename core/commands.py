import json
import shlex
import subprocess
import sys
import platform
from .messages import errors, message
from .ui import look, text
from .set_config import set_config
from rich.console import Console
from .storage import load_data, clear_memory

console = Console()
available_theme = ["retro", "pride", "poland", "indonesia", "russia", "italy", "france"]
        
class basic_commands:
    @staticmethod
    def cls():
        subprocess.run("cls" if platform.system() == "Windows" else "clear")

class handler:
    @staticmethod
    def handle_command(user_input):
        try:
            if user_input in ["exit", "return"]: #exit from the program
                sys.exit(0)
        
            if user_input == "cls": #clear screen
                basic_commands.cls()
                look.render_banner()
                return True
    
            if user_input.startswith("/set-api"): #set api key
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    message.usage_warn("/set-api <YOUR OPENROUTER API KEY>")
                    return True

                api_key = parts[1].strip()
                set_api("api_key", api_key)
                message.success("Success!")
                return True

            if user_input.startswith("/set-model"): #set ai model
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    message.usage_warn("/set-model <YOUR PREFERRED MODEL>")
                    return True

                model = parts[1].strip()
                set_config("model", model)
                message.success("Success!")
                return True
        
            if user_input.startswith("/set-site-url"):
                parts = user_input.split(maxsplit=1)
            
                if len(parts) < 2:
                    message.usage_warn("/set-site-name <YOUR SITE URL>")
                    return True
            
                url = parts[1].strip()
                set_site_url("site_url", url)
                message.success("Success!")
                return True
        
            if user_input.startswith("/set-site-name"):
                parts = user_input.split(maxsplit=1)
            
                if len(parts) < 2:
                    message.usage_warn("/set-site-name <YOUR SITE NAME>")
                    return True
            
                name = parts[1].strip()
                set_site_name("site_name", name)
                message.success("Success!")
                return True

            if user_input == "/check-api": #check api key
                get_data = load_data()
                console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key'][:20]}...")
                return True
        
            if user_input == "/check-api-nc": #check api key without censor
                get_data = load_data()
                console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key']}")
                return True
        
            if user_input.startswith("/change-banner"):
                parts = user_input.split(maxsplit=1)
            
                if len(parts) < 2:
                    message.usage_warn(f"/change-banner <YOUR PREFERRED THEME {available_theme}>")
                    return True
            
                theme = parts[1].strip()
                if theme not in available_theme:
                    errors.print_error(f"Please input available theme {available_theme}", __file__)
                    return True
                set_config("banner_theme", theme)
                message.success("Success!")
                message.warn("You may need to restart the program!")
                return True
            
            if user_input.startswith("/see-file"):
                base_parts = user_input.split()
                
                if len(base_parts) < 2:
                    message.usage_warn(f"/see-file <filename>")
                    return True
                
                base_parts.remove(base_parts[0])
                
                file = base_parts
                
                for i in file:
                    subprocess.run(['cat', i])
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
                        errors.print_error(e, __file__)
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
                        "/check-api-nc": "check the api key without censor",
                        "/set-model": "set or change the ai model",
                        "/set-site-url": "set or change program site url",
                        "/set-site-name": "set or change program site name",
                        "/change-banner": "change banner theme",
                        "/cmd": "run system command directly from the program",
                        "/reset": "reset conversation history",
                        "/see-file": "same function like 'cat' command but more simple",
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
        except Exception as e:
            errors.print_error(e, __file__)
            return True
