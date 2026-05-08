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
from rich.console import Console
from markdown_text_clean import clean_text

console = Console()
data_file = os.path.abspath("core/data_file.json")
PROMPT_FILE = os.path.abspath("core/prompt.txt")
MEMORY_FILE = os.path.abspath("core/memory.json")
MAX_MEMORY_MESSAGES = 200000

def load_data():
    try:
        util.if_datafile_not_exists()

        if os.path.exists(data_file) and os.path.getsize(data_file) == 0:
            raise json.JSONDecodeError("File is empty", "", 0)

    except Exception as e:
        errors.print_error(e)

    with open(data_file, 'r', encoding="utf-8") as data:
        return json.load(data)
    
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_memory(messages):
    try:
        if len(messages) > MAX_MEMORY_MESSAGES:
            messages = messages[-MAX_MEMORY_MESSAGES:]
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        errors.print_error(e)

def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        console.print(f"[green]Memory cleared![/green]")
    else:
        console.print(f"[yellow]No memory to clear[/yellow]")

def set_api(api_key):
    data_content = load_data()

    data_content['api_key'] = api_key
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)

def set_model(model):
    data_content = load_data()

    data_content['model'] = model

    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)

def get_prompt():
    if not os.path.exists(PROMPT_FILE):
        default_prompt = "You are tebac, a very helpfull and very kind ai that help people anytime."
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(default_prompt)
        return default_prompt
    
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
            else:
                return "You are tebac, a very helpfull and very kind ai that help people anytime."
            
    except Exception as e:
        print(f"{colors.red}Failed to read system prompt: {e}{colors.reset}")
        return "You are FreedomAI, an freedom unrestricted AI assistant that help people anytime."

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
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def check_if_its_command(user_input):
    if user_input in ["exit", "return"]:
        sys.exit(0)
        
    if user_input == "cls":
        basic_commands.cls()
        look.render_banner()
        return True

    if user_input.startswith("/set-api"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            console.print(f"[yellow]Usage: [/yellow][bold]/set-api API_KEY[/bold]")
            return True

        api_key = parts[1].strip()
        set_api(api_key)
        console.print("[bold green]Success![/bold green]")
        return True

    if user_input.startswith("/set-model"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            console.print(f"[yellow]Usage: [/yellow][bold]/set-model YOUR_PREFFERED_MODEL[/bold]")
            return True

        api_key = parts[1].strip()
        set_model(api_key)
        console.print("[bold green]Success![/bold green]")
        return True

    if user_input.startswith("/check-api"):
        get_data = load_data()
        console.print(f"[bold red]NO API KEY![/bold red]" if get_data['api_key'] == "<YOUR_API>" else f"[bold green]API_KEY[/bold green]: {get_data['api_key']}")
        return True
        
    if user_input == "/cmd":
        while True:
            try:
                given_cmd = console.input("[bold yellow]Enter command[/bold yellow]> ")
                
                if given_cmd in ["return", "exit"]:
                    return True
                
                cmd_args = shlex.split(given_cmd)
                if cmd_args:
                    subprocess.run(cmd_args)
                                   
            except Exception as e:
                print_error(e)
            except KeyboardInterrupt:
                print_keyboard_interrupt()
                return True

        
def chat():
    get_data = load_data()
    conversation_history = load_memory()
    basic_commands.cls()
    look.render_banner()
    
    license_gpl = """tebac  Copyright (C) 2026 nieatmaja
    This program comes with ABSOLUTELY NO WARRANTY.This is 
    free software, and you are welcome to redistribute it
    under certain conditions.\n"""
    
    print(license_gpl)

    if get_data['api_key'] == "<YOUR_API>":
        console.print(f"[bold]No api key specified, you may need to set your api key![/bold], run /set-api API_KEY")

    if get_data['model'] == "<YOUR_PREFFERED_MODEL>":
        console.print(f"[bold]No ai model specified, you may need to set ai model![/bold], run /set-model MODEL")

    while True:
        try:
            user_input = console.input(f"[bold blue]AI[/bold blue][bold red]@[/bold red][bold]{get_data['model']}[/bold][bold]>[/bold]\x20") # \x20 for SPACE
            
            if not user_input.strip():
                continue
            
            if check_if_its_command(user_input):
                continue
            
            with console.status("[blue]Thinking...[/blue]", spinner="dots"):
                response = call_api(user_input, conversation_history)
            
            if response:
                cleaned_response = clean_text(response)
                console.print(f"[[green]response[/green]]:\n")
                look.typing_print(cleaned_response)
                print("\n")
                
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
