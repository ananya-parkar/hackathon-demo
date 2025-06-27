from vosk import Model, KaldiRecognizer
 
import sounddevice as sd
 
import queue
 
import json
 
model_path = r"C:\Users\Ananya.Mehta\OneDrive - Parkar Digital\Desktop\AIPolicyAssistant\models\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
 
model = Model(model_path)
 
q = queue.Queue()
 
def callback(indata, frames, time, status):
 
    if status:
 
        print(status)
 
    q.put(bytes(indata))
 
def transcribe_from_mic(duration=5):
 
    samplerate = 16000
 
    rec = KaldiRecognizer(model, samplerate)
 
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
 
                           channels=1, callback=callback):
 
        print("🎙️ Speak now...")
 
        sd.sleep(duration * 1000)
 
        while not q.empty():
 
            data = q.get()
 
            if rec.AcceptWaveform(data):
 
                res = json.loads(rec.Result())
 
                return res.get("text", "")
 
        final_res = json.loads(rec.FinalResult())
 
        return final_res.get("text", "")
   
 
 
 
 