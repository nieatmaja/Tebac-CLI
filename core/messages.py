from rich.console import Console
import os
import json #prevent circular import by not importing .storage - load_data()

console = Console()

class message:
    @staticmethod
    def success(message: str) -> str:
        console.print(f"[bold green][✔]. {message}[/]")
        
    @staticmethod
    def warn(message: str) -> str:
        console.print(f"[bold yellow][!]. {message}[/]")
        
    @staticmethod
    def usage_warn(completions: str) -> str:
        console.print(f"[yellow]Usage: [/][bold]{completions}[/]")
        
    @staticmethod
    def ensure_api_model_valid() -> str:
        data_file = os.path.abspath("data/data_file.json")
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        if data['api_key'] == "<YOUR_API>" or not api_key.startswith("sk-or-v1"):
            __class__.warn(f"[bold]No valid openrouter api key specified, you may need to set your api key![/bold], run [white]/set-api[/] [purple]<API_KEY>[/]\n")

        if data['model'] == "<YOUR_PREFERRED_MODEL>":
            __class__.warn(f"[bold]No ai model specified, you may need to set ai model![/bold], run [white]/set-model [/][purple]<MODEL>[/]\n")
        
class errors:
    @staticmethod
    def print_error(message: str, file: __file__) -> str:
        console.print(f"[red][!] Error occurred on {file}: {message}[/]")

    @staticmethod
    def print_keyboard_interrupt() -> str:
        console.print("\n[red]Interrupted![/]")