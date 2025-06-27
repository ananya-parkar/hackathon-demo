# onnx_embedder.py
import torch
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

# Load quantized model and tokenizer
MODEL_PATH = r"C:\Users\Ananya.Mehta\OneDrive - Parkar Digital\Desktop\AIPolicyAssistant\models\onnx_model_quantized"
model = ORTModelForFeatureExtraction.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def encode(texts):
    """Replace SentenceTransformer's encode() with ONNX equivalent"""
    print("Texts received for encoding:", texts)
    if not texts:
        print("No texts provided for encoding.")
        return []
    
    if isinstance(texts, str):
        texts = [texts]
    
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pooling with attention mask
        last_hidden = outputs.last_hidden_state
        attention_mask = inputs["attention_mask"]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
        embeddings = (last_hidden * input_mask_expanded).sum(1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return embeddings.numpy()

