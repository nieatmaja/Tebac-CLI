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

import requests
import json
import subprocess
import sys
import os
import shlex
import sys
import platform
import time
from helpers import look, errors, basic_commands, util
from helpers import load_data, load_memory, save_memory, get_prompt
from rich.console import Console
from markdown_text_clean import clean_text

console = Console()
data_file = os.path.abspath("core/data_file.json")
get_data_global = load_data()

## Call openrouter api ##
def call_api(user_input, conversation_history):
    get_data = load_data()
    
    headers={
        "Authorization": f"Bearer {get_data['api_key']}",
        "HTTP-Referer": get_data['site_url'],
        "X-OpenRouter-Title": get_data['site_name'],
    }
    
    messages = [{"role": "system", "content": get_prompt()}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})
    
    data = {
        "model": get_data['model'],
        "messages": messages
    }
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=25
        )
    except requests.exceptions.Timeout:
        console.print("[red]Request timeout![/red]")
        
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def chat():
    basic_commands.cls()
    look.render_banner()
    
    if get_data_global['api_key'] == "<YOUR_API>" or "sk-or-v1" not in get_data_global['api_key']:
        console.print(f"[bold]No api key specified, you may need to set your api key![/bold], run /set-api API_KEY")

    if get_data_global['model'] == "<YOUR_PREFFERED_MODEL>":
        console.print(f"[bold]No ai model specified, you may need to set ai model![/bold], run /set-model MODEL")

    while True:
        try:
            conversation_history = load_memory()
            get_data = load_data()
            user_input = console.input(f"[bold blue]AI[/bold blue][bold red]@[/bold red][bold]{get_data['model']}[/bold][bold]>[/bold]\x20") # \x20 for SPACE
            
            if not user_input.strip():
                continue
            
            if util.check_if_its_command(user_input):
                continue

            try:
                with console.status("[blue]Thinking...[/blue]", spinner="dots"):
                    response = call_api(user_input, conversation_history)
            except KeyboardInterrupt:
                console.print("[red]Aborted[/red]")
                continue
            
            if response:
                cleaned_response = clean_text(response)
                console.print(f"[[green]response[/green]]:\n")
                look.typing_print(cleaned_response)
                print("")
                
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                save_memory(conversation_history)
            
        except Exception as e:
            errors.print_error(e)
        except KeyboardInterrupt:
            errors.print_keyboard_interrupt()
            sys.exit(0)
            
if __name__ == '__main__':
    chat()
