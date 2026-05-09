from rich.console import Console

console = Console()

class errors:
    @staticmethod
    def print_error(message) -> str:
        console.print(f"[red]Error occurred: {message}[/red]")

    @staticmethod
    def print_keyboard_interrupt() -> str:
        console.print("\n[red]Interrupted, exiting...[/red]")