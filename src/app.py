import streamlit as st

from PyPDF2 import PdfReader
import os
from backend.upload import save_uploaded_files
from backend.process import chunk_text_with_sources, create_faiss_index
from backend.retrieval import search_similar_chunks
from backend.ollama_handler import query_ollama_stream
from backend.ner_utils import extract_entities
from backend.utils import extract_text_from_file
from backend.lang_utils import detect_language
from backend.logger import log_interaction
from backend.transcribe import transcribe_from_mic

def format_chat_history(messages):
    formatted = []
    for i in range(0, len(messages), 2):
        if i + 1 < len(messages):
            user_msg = messages[i]['content']
            ai_msg = messages[i+1]['content']
            formatted.append(f"**You:**\n{user_msg}\n\n**AI:**\n{ai_msg}\n\n---")
    return "\n".join(formatted)

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title="📄 Doc Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== GLOBAL SESSION STATE ======
if "file_text_map" not in st.session_state:
    st.session_state.file_text_map = {}
if "ner_summary" not in st.session_state:
    st.session_state.ner_summary = {}
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = []
if "files_processed" not in st.session_state:
    st.session_state.files_processed = False

# ====== CUSTOM CSS ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
div[data-testid="stAppViewContainer"] {
    background-color: #f8f9fa;
    font-family: 'Inter', sans-serif;
}
.block-container { padding-top: 4rem !important; }  /* Increased top padding */
[data-testid="stFileUploader"] { margin-top: 0 !important; padding-top: 0 !important; }
[data-testid="stFileUploader"] > div { margin-top: 0 !important; padding-top: 0 !important; }
[data-testid="stSidebar"] { background-color: #317987 !important; }
[data-testid="stSidebar"] > div:first-child {
    background-color: #007091 !important;
    border-radius: 0 12px 12px 0;
    padding: 1.5em;
}
[data-testid="stSidebar"] * { color: white !important; }
.upload-header-tint {
    background-color: #e6f2ff;
    padding: 24px 32px 16px 32px;
    border-radius: 10px;
    margin-bottom: 24px;
}
h1 { color: #336699; text-align: center; font-size: 42px; margin-bottom: 0.5em; }
h2, h3 { color: #495057; margin-top: 1em; }
.stButton>button {
    background-color: #336699;
    color: white;
    border-radius: 6px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    margin: 0.5em 0;
}
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    border: 2px solid #aad4ff;
    border-radius: 8px;
    padding: 10px;
    font-size: 16px;
    background-color: #ffffff;
}
[data-testid="stFileUploader"] {
    background: linear-gradient(90deg, #e6f2ff 0%, #f8fafc 100%) !important;
    border-radius: 12px !important;
    border: 2px dashed #99ccff !important;
    box-shadow: 0 2px 8px rgba(51,102,153,0.06);
    padding: 28px 18px 18px 18px !important;
    margin-bottom: 20px !important;
    font-size: 15px !important;
    color: #336699 !important;
    max-width: 100% !important;
}
[data-testid="stFileUploader"] > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    flex: 1;
    text-align: left;
    font-size: 1rem;
    color: #336699;
    padding-left: 10px;
    font-weight: 500;
}
[data-testid="stFileUploaderDropzone"] button {
    flex-shrink: 0;
    background-color: #317987 !important;
    color: white !important;
    border-radius: 7px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-right: 10px;
    cursor: pointer;
    border: none !important;
    box-shadow: 0 2px 8px rgba(51,102,153,0.08);
    transition: background 0.2s;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #255e6a !important;
}
[data-testid="stFileUploaderDropzone"] > div > div > div {
    display: none !important;
}
[data-testid="stFileUploader"] > div > div > div:nth-child(3) {
    margin-top: 8px;
    color: #317987;
    font-size: 0.9rem;
    text-align: left;
    padding-left: 10px;
    background: #d9ecff;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 4px;
}
[data-testid="stFileUploader"] ul,
[data-testid="stFileUploader"] li,
[data-testid="stFileUploader"] span {
    font-size: 13px !important;
    color: #222 !important;
}
h4, .stMarkdown h4, [data-testid="stFileUploaderLabel"] {
    color: #336699 !important;
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
    letter-spacing: 0.5px;
}
.stMarkdown { font-size: 16px; line-height: 1.6; }
.stSuccess {
    border-radius: 8px;
    padding: 1em;
    background-color: #d4edda;
    color: #155724;
}
.stExpander {
    border: 1px solid #aad4ff;
    border-radius: 8px;
    background-color: #ffffff;
}
.file-summary {
    background-color: #e6f2ff;
    border-radius: 8px;
    padding: 1em;
    margin: 1em 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.answer-box {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1em;
    border: 1px solid #aad4ff;
    margin: 1em 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.entity-list {
    font-family: monospace;
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1em;
    margin: 0.5em 0;
}
.question-area {
    min-height: 120px;
}
.section-anchor {
    position: relative;
    top: -100px;
    visibility: hidden;
}
.nav-link {
    display: inline-block;
    background-color: white !important;
    color: black !important;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    text-decoration: none !important;
    text-align: center;
    transition: background-color 0.2s;
    margin: 2px;
    min-width: 200px;
    flex:1;
}
.nav-link:hover {
    background-color: #f0f0f0 !important;
}
.file-summary {
    background-color: #e6f2ff;  
    border-radius: 6px;
    padding: 0.5em;            
    margin: 0.5em 0;            
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);  
    font-size: 14px;            
    color: #666;                
}
.chat-history-panel {
    max-height: 320px;
    overflow-y: auto;
    background: #f4f8fc;
    border-radius: 8px;
    border: 1px solid #aad4ff;
    padding: 16px;
    margin-top: 10px;
    font-size: 1rem;
}
::-webkit-scrollbar { width: 8px; background: #e6f2ff; }
::-webkit-scrollbar-thumb { background: #aaccee; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown("## 🛠️ Navigation")
    st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px;">
<a href="#upload-section" class="nav-link">📂 Upload PDFs</a>
<a href="#question-section" class="nav-link">🧠 Ask Questions</a>
<a href="#chat-history-section" class="nav-link">💬 Chat history</a>
</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("""
Unlock instant insights from any document—just upload, ask, and let AI do the rest! Experience seamless, intelligent answers from PDFs, images, Word files, and more—all in one place.
""")

# ====== MAIN CONTENT ======
st.markdown("""
<div style='
    background: linear-gradient(90deg, #e6f2ff 0%, #f8fafc 100%);
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(51,102,153,0.06);
    text-align: center;
'>
    <span style='font-size: 2.1rem; color: #336699; font-weight: 700; letter-spacing: 1px;'>
        Welcome to <span style='color:#007091;'> AI Policy Assistant</span>!
    </span>
    <br>
    <span style='font-size: 1.18rem; color: #333; font-weight: 500;'>
        Upload your PDFs, ask questions, and get <span style='color:#317987;'>intelligent answers powered by AI</span>.
    </span>
</div>
""", unsafe_allow_html=True)

# ====== UPLOAD SECTION ======
st.markdown('<div class="section-anchor" id="upload-section"></div>', unsafe_allow_html=True)
st.markdown("#### 📂 Upload Files")
uploaded_files = st.file_uploader(
    "",
    type=["pdf", "docx", "txt", "md", "html", "xls", "xlsx", "pptx", "jpg", "jpeg", "png", "tiff", "zip", "tif", "htm"],
    accept_multiple_files=True
)

# ====== FILE PROCESSING LOGIC (updated) ======
# Reset flag if new files are uploaded
if uploaded_files and uploaded_files != st.session_state.get("uploaded_files_cache"):
    st.session_state.files_processed = False
    st.session_state.uploaded_files_cache = uploaded_files

# Only process if not already processed
if uploaded_files and not st.session_state.files_processed:
    with st.spinner("🔍 Processing uploaded files..."):
        st.session_state.file_text_map.clear()
        st.session_state.ner_summary.clear()
        file_paths = save_uploaded_files(uploaded_files)
        for path in file_paths:
            try:
                text = extract_text_from_file(path)
                print("Extracted text for", os.path.basename(path), ":", text)
                st.session_state.file_text_map[os.path.basename(path)] = text
            except Exception as e:
                print(f"Skipping {path}: {e}")
        # Run NER
        for filename, text in st.session_state.file_text_map.items():
            entities = extract_entities(text)
            st.session_state.ner_summary[filename] = entities
        # Chunk + FAISS Index
        chunks = chunk_text_with_sources(st.session_state.file_text_map)
        print("Chunks generated from all files:")  
        for chunk in chunks:
            print(chunk)
        create_faiss_index(chunks)
    st.session_state.files_processed = True
    st.success("✅ Processed!")

# ====== FILE SUMMARY ======
if st.session_state.file_text_map:
    files_str = ", ".join(
        f"{name} ({len(text)} chars)" for name, text in st.session_state.file_text_map.items()
    )
    st.caption(f"Files: {files_str}")

# ====== QUESTION INPUT ======
st.markdown(
    '<div class="voice-prompt">🎤 <b>Prefer speaking?</b> Click below to record your question by voice.</div>',
    unsafe_allow_html=True
)

if st.button("Record Voice "):
    st.session_state.transcribed_text = ""  # Clear before recording
    with st.spinner("Listening... Please speak your question clearly."):
        text = transcribe_from_mic(duration=7)
        st.session_state.transcribed_text = text
st.markdown("#### 💬 Ask a Question")
user_question = st.text_area(
    "Type your question below:",
    value=st.session_state.transcribed_text,
    placeholder="What would you like to know?",
    height=150
)

if st.button("Ask Now", type="primary"):
    if user_question:
        with st.spinner("Generating answer..."):
            matched_chunks = search_similar_chunks(user_question)
            print("Chunks matched for question:", user_question)
            for c in matched_chunks:
                print(c)
           
            # Build context with page numbers
            context_str = "\n\n".join([f"[{c['source']} (Page {c['page']})]\n{c['text']}" for c in matched_chunks])
           
            # Combine entities
            flat_entities = [f"{label}: {text}" for ents in st.session_state.ner_summary.values() for text, label in ents]
            entity_context = "\n\n".join(flat_entities) if flat_entities else "None"
           
            prompt = f"""
                You are an expert document analyst. The following is text extracted from one or more documents, which may include PDFs, DOCX, HTML, images (via OCR), spreadsheets, and other formats. The extracted content may contain lists, tables, paragraphs, bullet points, or unstructured fragments.
 
                Your task is to:
                - Carefully analyze and synthesize ALL available information from the provided document text, regardless of format.
                - Answer the user's question as accurately and comprehensively as possible, using only the information present in the extracted text.
                - If the answer is found across multiple sections or formats (e.g., bullet points, tables, images), combine the information into a clear, coherent answer.
                - If the answer is not explicitly stated but can be reasonably inferred from the available data, provide the best possible inference and explain your reasoning.
                - Only say "The answer is not available in the provided documents." if you are absolutely certain the answer is not present.
                - Answer in the same language as the user's question.
 
                Extracted Document Text:
                {context_str}
 
                User Question:
                {user_question}
 
                Your Answer:
                """
            response_container = st.empty()
            full_response = ""
            for token in query_ollama_stream(prompt):
                full_response += token
                response_container.markdown(f"<div class='answer-box'>{full_response}▌</div>", unsafe_allow_html=True)
           
            # Group and format the sources
            from collections import defaultdict
            source_dict = defaultdict(set)
            for chunk in matched_chunks:
                filename = chunk['source']
                page_num = str(chunk['page'])
                source_dict[filename].add(page_num)
            formatted_sources = []
            for filename, pages in source_dict.items():
                sorted_pages = sorted(pages, key=lambda x: int(x))
                if len(sorted_pages) > 1:
                    page_list = ", ".join(sorted_pages)
                    formatted_sources.append(f"{filename} (Pages {page_list})")
                else:
                    formatted_sources.append(f"{filename} (Page {sorted_pages[0]})")
            formatted_sources_str = "\n".join(formatted_sources)
            full_response_with_sources = f"{full_response}\n\n*Sources:*\n{formatted_sources_str}"
           
            # Handle fallback response
            fallback = "The answer is not available in the provided documents."
            cleaned_response = full_response_with_sources.strip()
            if cleaned_response.lower().startswith(fallback.lower()) and len(cleaned_response) > len(fallback) + 10:
                cleaned_response = cleaned_response[len(fallback):].strip(" .\n")
            if not cleaned_response or cleaned_response.lower().startswith(fallback.lower()):
                response_container.markdown(f"<div class='answer-box'>{fallback}</div>", unsafe_allow_html=True)
            else:
                response_container.markdown(f"<div class='answer-box'>{cleaned_response}</div>", unsafe_allow_html=True)
           
            # Log interaction (without page numbers)
            log_sources = list(set([chunk['source'] for chunk in matched_chunks]))
            log_interaction(user_question, full_response, log_sources)
            # ====== SAVE TO CHAT HISTORY ======
            st.session_state.messages.append({"role": "user", "content": user_question})
            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})

# ====== CHAT HISTORY PANEL ======
st.markdown('<div id="chat-history-section"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="margin-top:24px; font-size:1.2rem; color:#336699; font-weight:600;">
        💬 Chat History
    </div>
    """,
    unsafe_allow_html=True
)
formatted_chat = format_chat_history(st.session_state.messages)
chat_history_markdown = f"""
<div class="chat-history-panel">
{formatted_chat}
</div>
"""
st.markdown(chat_history_markdown, unsafe_allow_html=True)
