import faiss
import numpy as np
import pickle
from backend.onnx_embedder import encode
 
def search_similar_chunks(query, index_path="vector_store/index.faiss", top_k=5):
    # Load index and chunk data
    index = faiss.read_index(index_path)
    with open(index_path.replace(".faiss", ".pkl"), "rb") as f:
        data = pickle.load(f)
        chunks = data["chunks"]
        page_info = data["page_info"]
   
    # Encode query and search
    query_embedding = encode([query])[0]
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), top_k)
   
    # Return chunks with page info
    return [{
        "text": chunks[i]["text"],
        "source": chunks[i]["source"],
        "page": chunks[i]["page"]  # Include page number
    } for i in indices[0]]
 
 