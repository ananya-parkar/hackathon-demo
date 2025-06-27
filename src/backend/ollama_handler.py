import requests
import json
 
def query_ollama_stream(prompt, model="llama3.2"):
    """Streams response from Ollama API"""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True 
    }
   
    try:
        response = requests.post(
            url,
            json=payload,
            stream=True,
            timeout=700
        )
        response.raise_for_status()
       
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if not data.get("done", False):
                    yield data.get("response", "")
   
    except Exception as e:
        yield f"❌ Error: {str(e)}"