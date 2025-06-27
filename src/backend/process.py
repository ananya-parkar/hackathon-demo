from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.onnx_embedder import encode
import faiss
import numpy as np
import os
import pickle
 
# 🧠 Chunking with file info
def chunk_text_with_sources(file_text_map, chunk_size=300, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    all_chunks = []
    for filename, pages in file_text_map.items():
        # Fix: If pages is a string, wrap it as a list of one dict
        if isinstance(pages, str):
            pages = [{"text": pages, "page": 1}]
        elif isinstance(pages, dict):  # If it's a dict, wrap in list
            pages = [pages]
        for page_data in pages:
            text = page_data["text"]
            page_num = page_data["page"]
            chunks = splitter.split_text(text)
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "source": filename,
                    "page": page_num
                })
    return all_chunks
 
 
# 🔍 Embed only the chunk texts
def embed_chunks(chunks_with_source):
   texts = [chunk["text"] for chunk in chunks_with_source if chunk.get('text','').strip()]
   print("Texts to embed:", texts)
 
   if not texts:
       print("No valid texts to embed.")
       return []
   return encode(texts)
 
 
# 🧠 Build & save FAISS index + source data
def create_faiss_index(chunks_with_source, save_path="vector_store/index.faiss"):
    if not chunks_with_source:
        print("No chunks_with_source provided.")
        return
   
    # Embed only the text content
    embeddings = embed_chunks(chunks_with_source)
   
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
   
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    faiss.write_index(index, save_path)
   
    # Save chunks with source AND page info
    with open(save_path.replace(".faiss", ".pkl"), "wb") as f:
        pickle.dump({
            "chunks": chunks_with_source,
            "page_info": [{"source": c["source"], "page": c["page"]} for c in chunks_with_source]
        }, f)
 
 