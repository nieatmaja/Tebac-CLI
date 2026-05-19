import json
import os
import sys
from rich.console import Console
from .messages import errors, message
from .helpers import ensure_datafile_exists, ensure_memoryfile_exists
from .get_file_loc import get_file_loc

console = Console()

data_file = get_file_loc("data_file")
MEMORY_FILE = get_file_loc("memory")

## Load configuration data from data_file.json ##
def load_data():
    try:
        ensure_datafile_exists()

        if os.path.exists(data_file) and os.path.getsize(data_file) == 0:
            raise json.JSONDecodeError("File is empty", "", 0)

    except Exception as e:
        errors.print_error(f"Error loading data ({e})", __file__)

    with open(data_file, 'r', encoding="utf-8") as data:
        return json.load(data)

## Load conversation history from memory.json ##    
def load_memory():
    try:
        ensure_memoryfile_exists()
    except Exception as e:
        errors.print_error(f"Error loading memory ({e})", __file__)
        
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

## Save conversation history to memory.json ##
def save_memory(messages):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        errors.print_error(f"Error saving memory ({e})", __file__)

# Clear all saved conversation history in memory.json
def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        message.success("Memory cleared!")
    else:
        message.warn("No memory to clear!")
    return []