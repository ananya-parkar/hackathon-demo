from backend.transcribe import transcribe_from_mic
 
text = transcribe_from_mic(duration=5)
print("✅ Your transcription:", text)
 
 
 