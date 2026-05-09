import os
import json

data_file = os.path.abspath("core/data_file.json")

def if_datafile_not_exists():
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
