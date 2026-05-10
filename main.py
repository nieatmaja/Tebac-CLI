# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 nieatmaja
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sys
from core.api import call_api
from core.storage import load_data, load_memory, save_memory
from core.commands import basic_commands, handler
from core.ui import look, text
from core.errors import errors
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def chat():
    config = load_data()
    basic_commands.cls()
    look.render_banner()
    
    if config['api_key'] == "<YOUR_API>" or "sk-or-v1" not in config['api_key']:
        console.print(f"[bold]No valid openrouter api key specified, you may need to set your api key![/bold], run /set-api API_KEY")

    if config['model'] == "<YOUR_PREFFERED_MODEL>":
        console.print(f"[bold]No ai model specified, you may need to set ai model![/bold], run /set-model MODEL")

    while True:
        try:
            conversation_history = load_memory()
            get_data = load_data()
            user_input = console.input(f"[bold blue]AI[/bold blue][bold red]@[/bold red][bold]{get_data['model']}[/bold][bold]>[/bold]\x20") # \x20 for SPACE
            
            if not user_input.strip():
                continue
            
            if handler.handle_command(user_input):
                continue

            try:
                with console.status("[blue]Thinking...[/blue]", spinner="dots"):
                    response = call_api(user_input, conversation_history)
            except KeyboardInterrupt:
                console.print("[red]Aborted[/red]")
                continue
            
            if response:
                console.print(f"[[green]response[/green]]:\n")
                text.typing_print(response)
                print("")
                
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                save_memory(conversation_history)
                
        except KeyboardInterrupt:
            errors.print_keyboard_interrupt()
            sys.exit(0)    
        except Exception as e:
            errors.print_error(e)
        
            
if __name__ == '__main__':
    chat()
