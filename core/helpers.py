import os
import json

def ensure_datafile_exists():
    data_file = os.path.abspath("data/data_file.json")
    if not os.path.exists(data_file):
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
            
        default_data = {
            "api_key": "<YOUR_API>",
            "site_url": "https://github.com/nieatmaja",
            "site_name": "tebac",
            "model": "<YOUR_PREFFERED_MODEL>"
        }
            
        with open(data_file, 'w') as f:
            json.dump(default_data, f, indent=4)
            
        return default_data
    
def ensure_fileloc_exists():
    data_file_loc = os.path.abspath("data/file_loc.json")
    if not os.path.exists(data_file_loc):
        os.makedirs(os.path.dirname(data_file_loc), exist_ok=True)
            
        default_data = {
            "config_file_location": "data/data_file.json",
            "prompt_file_location": "data/prompt.txt",
            "memory_file_location": "data/memory.json"
        }
            
        with open(data_file_loc, 'w') as f:
            json.dump(default_data, f, indent=4)
            
        return default_data
    
def ensure_memoryfile_exists():
    memory_file = os.path.abspath("data/memory.json")
    if not os.path.exists(memory_file):
        os.makedirs(os.path.dirname(memory_file), exist_ok=True)
            
        default_data = []
            
        with open(memory_file, 'w') as f:
            json.dump(default_data, f, indent=4)
            
        return default_data
