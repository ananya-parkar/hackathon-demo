# backend/logger.py
import json
import datetime
import os
from langdetect import detect 

def log_interaction(query, answer, sources, log_path="qa_log.json"):
    try:
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                logs = json.load(f)
        else:
            logs = []
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "sources": sources,
        "detected_language": detect(query)  # Add language detection
    })
    
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
