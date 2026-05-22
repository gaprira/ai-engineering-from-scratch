import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "nvidia/nemotron-3-super-120b-a12b:free", 
       "messages": [
        {"role": "system", "content": "Ты — грубый пират. Отвечай только пиратским сленгом."},
        {"role": "user", "content": "скажи что нибдь по пиратски"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.json()['choices'][0]['message']['content'])