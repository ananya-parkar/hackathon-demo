import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.2",
    "prompt": "Hello, how are you?",
    "stream": False
}
resp = requests.post(url, json=payload, timeout=60)
print(resp.status_code)
print(resp.text)
