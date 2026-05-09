import json
import os
from storage import load_data

data_file = os.path.abspath("core/data_file.json")

## Function to set API KEY##
def set_api(api_key):
    data_content = load_data()

    data_content['api_key'] = api_key
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)

# Function to set AI MODEL ##
def set_model(model):
    data_content = load_data()

    data_content['model'] = model

    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)
        
def set_site_url(url):
    data_content = load_data()
    
    data_content['site_url'] = url
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)
        
def set_site_name(name):
    data_content = load_data()
    
    data_content['site_name'] = name
    
    with open(data_file, 'w') as data:
        json.dump(data_content, data, indent=4)