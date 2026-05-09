import json
import requests
import os
from storage import load_data

PROMPT_FILE = os.path.abspath("core/prompt.txt")

## Get AI prompt from prompt.txt ##
def get_prompt():
    if not os.path.exists(PROMPT_FILE):
        default_prompt = "You are tebac, a very helpful and very kind ai that help people anytime."
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(default_prompt)
        return default_prompt
    
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
            else:
                return "You are tebac, a very helpful and very kind ai that help people anytime."
            
    except Exception as e:
        print(f"{colors.red}Failed to read system prompt: {e}{colors.reset}")
        return "You are tebac, a very helpful and very kind ai that help people anytime."

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