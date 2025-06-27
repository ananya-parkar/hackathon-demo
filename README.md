
# AI Policy Assistant

**AI Policy Assistant** is your intelligent workplace companion—an app that instantly answers your questions about company policies, handbooks, and internal documents.  
Just upload your files (PDFs, DOCX, images, and more), ask your question (by text or voice), and get clear, reliable answers—always with source references.

## Features

- 📁 **Multi-format support**: Works with PDFs, DOCX, TXT, spreadsheets, and images (even scans/photos).
- 🎙️ **Voice-to-text input**: Ask your policy questions out loud—no typing required.
- 💬 **Multilingual Q&A**: Ask in your preferred language, get answers in the same language.
- 🔍 **Semantic search & entity extraction**: Finds the most relevant policy text, highlights key terms, dates, and names.
- 📜 **Chat history**: Scroll back through your previous questions and answers.
- 🚀 **Private & local**: All processing is done on your machine—no cloud, no data leaks.

## Installation

1. **Prerequisites**
   - Python 3.8+
   - [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (for image/PDF text extraction)
   - [Ollama](https://ollama.com/) with the Llama 3 model (`ollama run llama3`)
   - [Vosk model](https://alphacephei.com/vosk/models) for speech recognition

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Model setup**
   - Place the **Vosk model** in `src/models/vosk-model-small-en-us-0.15/`
   - Place the **ONNX embedding model** in `src/models/onnx_model_quantized/`

4. **Configuration**
   - Create a `.env` file (if needed) with:
     ```
     TESSERACT_CMD_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
     ONNX_MODEL_PATH=src/models/onnx_model_quantized
     ```

## Usage

1. **Start the assistant**
   ```bash
   streamlit run src/app.py
   ```
2. **Upload your policy documents** (PDF, DOCX, images, etc.)
3. **Ask your question**—type it or use the voice button
4. **Get instant answers**—with references to the exact document and page

## Project Structure

```
AIPolicyAssistant/
├── src/         # Application source code
│   ├── backend/
│   ├── models/
│   └── tests/
├── docs/        # Documentation
├── data/        # Sample documents
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuration

- **Tesseract OCR**: Make sure the path in `.env` matches your Tesseract installation.
- **ONNX Model**: Place the ONNX model in the correct directory as above.
- **Vosk Model**: Download and extract the Vosk speech model for voice recognition.

## Troubleshooting

- **OCR issues**: Double-check the Tesseract install and `.env` path.
- **Model errors**: Ensure ONNX and Vosk models are in `src/models/`.
- **Voice recognition**: Grant microphone permissions to your terminal/app.
- **Ollama errors**: Make sure Ollama is running and the Llama 3 model is pulled.

## Why AI Policy Assistant?

- **Empower employees** to get instant, accurate answers about HR, benefits, and company rules.
- **Reduce HR workload**—let the assistant handle routine queries.
- **Keep sensitive data private**—everything runs locally, nothing goes to the cloud.

**Built by Team AInsteins.**
