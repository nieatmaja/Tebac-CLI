import json
import os
from .messages import errors
from .storage import load_data

data_file = os.path.abspath("data/data_file.json")

def set_config(config: str, value: str):
    try:
        data_content = load_data()
    
        if config not in data_content.keys():
            return errors.print_error("Invalid config!", __file__)
    
        data_content[config] = value
    
        with open(data_file, 'w') as data:
            json.dump(data_content, data, indent=4)
    except Exception as e:
        return errors.print_error(e, __file__)