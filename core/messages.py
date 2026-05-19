from rich.console import Console

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
        
class errors:
    @staticmethod
    def print_error(message: str, file: __file__) -> str:
        console.print(f"[red][!] Error occurred on {file}: {message}[/]")

    @staticmethod
    def print_keyboard_interrupt() -> str:
        console.print("\n[red]Interrupted![/]")