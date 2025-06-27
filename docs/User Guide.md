
AI Policy Assistant – User Guide
Welcome to AI Policy Assistant! This app lets you upload documents and images, then ask questions to get intelligent, AI-powered answers based on the content you provide.

Table of Contents
- Getting Started
- Supported File Types
- Uploading Files
- Asking Questions
- How Answers Are Generated
- Troubleshooting
- FAQ
- Contact & Support

Getting Started
1. Open the Document Analyzer app (usually via a link or by running streamlit run app_ananya.py).
2. You’ll see the main interface with options to upload files and ask questions.

Supported File Types
You can upload the following file types (up to 200MB each):
- Documents: PDF, DOCX, TXT, MD, HTML, HTM, XLS, XLSX, PPTX, ZIP
- Images: JPG, JPEG, PNG, TIFF, TIF

Uploading Files
1. Click “Upload Files” or drag-and-drop your files into the upload area.
2. Wait for the app to process your files. You’ll see a ✅ “Processed!” message when done.
3. The app will show the list of uploaded files and the number of characters/text extracted from each.

Tip: For best results, use clear, high-quality scans for images. Handwritten or blurry images may not extract text well.

Asking Questions
1. Type your question in the “Ask a Question” box.
2. Click “Generate”.
3. The app will analyze your uploaded documents and display an answer based on their content.

Example Questions:
- “What is the workflow described in the document?”
- “Summarize the main points.”
- “What are the characteristics of a good culture?”

How Answers Are Generated
- The app extracts text from all uploaded files using OCR (for images) or text extraction (for documents).

- When you ask a question, an AI model searches the extracted content for relevant information.

- If a detailed answer is found, it is displayed.

- If only a partial answer is available, the app will show the best summary it can find.

- If no relevant information is found, you’ll see:
“The answer is not available in the provided documents.”

Note:
The app now avoids showing the fallback message if any useful answer or summary is available!

Troubleshooting
- No Text Extracted from Image:
Ensure your image is clear, high-contrast, and contains printed text. If you see “0 chars” next to a file, the app could not extract text.

- Getting Only the Fallback Message:
This means the app could not find a relevant answer in your files. Try uploading more detailed documents or clearer images.

- File Not Supported/Error:
Check the file type and size. Only supported file types up to 200MB are accepted.

FAQ
Q: Can I upload multiple files?
A: Yes! Upload as many as you want (within size limits). The app will search all files for answers.

Q: Does the app work with handwritten notes?
A: OCR works best with printed text. Handwritten text may not be extracted accurately.

Q: Why do I get “No chunks generated!”?
A: This means the app could not extract any text from your files. Try using different files or improving image quality.

Q: How is my data used?
A: Uploaded files are processed only for answering your questions and are not stored permanently.

Contact & Support
For questions, feedback, or support, contact the development team, Team AInsteins.

Enjoy using AI Policy Assistant!
If you have suggestions for improvement, let us know.
