import json
import os
import sys
from .messages import errors
from .helpers import ensure_fileloc_exists

def get_file_loc(filename: str):
    if not isinstance(filename, str):
        raise ValueError("Please only input str in function get_file_loc(!str)!")
    
    try:
        ensure_fileloc_exists()
    except Exception as e:
        errors.print_error(f"ensure_fileloc_exists on get_file_loc ({e})", __file__)
        sys.exit(0)
        
    try:
        data_file = os.path.abspath("data/file_loc.json")
    
        with open(data_file, 'r') as data:
            file = json.load(data)
        
        if filename == "data_file":
            return os.path.abspath(file["config_file_location"])
        elif filename == "prompt":
            return os.path.abspath(file["prompt_file_location"])
        elif filename == "memory":
            return os.path.abspath(file["memory_file_location"])
        else:
            errors.print_error("Invalid argument for filename! ['data_file.json', 'prompt.txt', 'memory.json']", __file__)
    except Exception as e:
        errors.print_error(f"Error on returning abspath from json ({e})", __file__)
        sys.exit(0) 