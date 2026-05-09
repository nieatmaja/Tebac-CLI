import json
from errors import errors
import os
from rich.console import Console
from helpers import if_datafile_not_exists

console = Console()

data_file = os.path.abspath("core/data_file.json")
MEMORY_FILE = os.path.abspath("core/memory.json")

## Load configuration data from data_file.json ##
def load_data():
    try:
        if_datafile_not_exists()

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