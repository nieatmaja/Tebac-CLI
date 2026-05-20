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
from .banner_theme import banner_theme

console = Console()
        
class basic_commands:
    @staticmethod
    def cls():
        subprocess.run("cls" if platform.system() == "Windows" else "clear")

class handler:
    @staticmethod
    def handle_command(user_input):
        try:
            #COMMANDS THAT DOESN'T NEED ARGUMENTS#
            def exit_program():
                if user_input in ["exit", "return"]: #exit from the program
                    sys.exit(0)
        
            def cls(): #clear screen
                basic_commands.cls()
                look.render_banner()
                return True
            
            #print api key with splitted text
            def check_api():
                get_data = load_data()
                console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key'][:20]}...")
                return True
        
            #print api key without splitting the text
            def check_api_nc():
                get_data = load_data()
                console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key']}")
                return True
            
            #reset conversation history
            def reset():
                clear_memory()
                return True
            
            #run system commands
            def cmd():
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

            #print all available commands
            def help():
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
                    },
                    "keyboard_shortcut": {
                        "CTRL + C": "Aborting call or exit from the program"
                    }
                }
        
                console.print("\n[[bold]Basic command[/bold]]\n")
                for key, value in available_command["basic_command"].items():
                    console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]") #print basic commands section
            
                print("")
                
                console.print("[[bold]Advanced command[/bold]]\n")
                for key, value in available_command["advanced_command"].items():
                    console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]") #print advanced commands section

                print("")

                console.print("[[bold]Keyboard Shortcut[/bold]]\n")
                for key, value in available_command["keyboard_shortcut"].items():
                    console.print(f"[bold]{key}[/bold] - [bold blue]{value}[/bold blue]") #print keyboard shortcut section

                print("")
            
                return True
            
            ## COMMANDS THAT REQUIRE ARGUMENTS ##
            def set_api(args):
                if len(args) < 0:
                    message.usage_warn("/set-api <YOUR OPENROUTER API KEY>")
                    return True
                elif len(args) > 1:
                    message.warn("Please only input 1 argument!")
                    return True

                api_key = args[0].strip()
                set_config("api_key", api_key)
                message.success("Success!")
                return True
            
            #change/set the ai model in data/data_file.json
            def set_model(args):
                
                if len(args) < 0:
                    message.usage_warn("/set-model <YOUR PREFERRED MODEL>")
                    return True
                elif len(args) > 1:
                    message.warn("Please only input 1 argument!")
                    return True

                model = args[0].strip()
                set_config("model", model)
                message.success("Success!")
                return True

            #change/set site url in data/data_file.json
            def set_site_url(args):
                if len(args) < 0:
                    message.usage_warn("/set-site-name <YOUR SITE URL>")
                    return True
                elif len(args) > 1:
                    message.warn("Please only input 1 argument!")
                    return True
            
                url = args[0].strip()
                set_config("site_url", url)
                message.success("Success!")
                return True
            
            #change/set site name in data/data_file.json
            def set_site_name(args):
                if len(parts) < 0:
                    message.usage_warn("/set-site-name <YOUR SITE NAME>")
                    return True
                elif len(args) > 1:
                    message.warn("Please only input 1 argument!")
                    return True
            
                name = args[0].strip()
                set_config("site_name", name)
                message.success("Success!")
                return True

            #change/set banner theme
            def change_banner(aegs):
                if len(args) < 0:
                    message.usage_warn(f"/change-banner <YOUR PREFERRED THEME {available_theme}>")
                    return True
                elif len(args) > 1:
                    message.warn("Please only input 1 argument!")
                    return True
            
                theme = args[0].strip()
                theme_list = banner_theme.available_theme().keys()
                
                if theme not in theme_list:
                    errors.print_error(f"Please input available theme {available_theme}", __file__)
                    return True
                
                set_config("banner_theme", theme)
                message.success("Success!")
                message.warn("You may need to restart the program!")
                return True
            
            #available commands
            COMMANDS =  {
                "args_not_required": {
                    "exit": exit_program,
                    "cls": cls,
                    "/cmd": cmd,
                    "/reset": reset,
                    "/help": help,
                },
                "args_required": {
                    "/set-api": set_api,
                    "/check-api": check_api,
                    "/check-api-nc": check_api_nc,
                    "/set-model": set_model,
                    "/set-site-url": set_site_url,
                    "/set-site-name": set_site_name,
                    "/change-banner": change_banner  
                }
            }
            parts = user_input.split() #split the text into subpieces
            command = parts[0] #get the command name from first index
            args = parts[1:] #get the arguments after first index 
            if command in COMMANDS['args_not_required'].keys():
                try:
                    
                    COMMANDS['args_not_required'][command]()
                    return True
                
                except Exception as e:
                    errors.print_error(e, __file__)
                    return True
                
            elif command in COMMANDS['args_required'].keys():
                try:
                    
                    COMMANDS['args_required'][command](args)
                    return True
                
                except Exception as e:
                    errors.print_error(e, __file__)
                    return True
            
        except Exception as e:
            errors.print_error(e, __file__)
            return True
