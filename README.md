# Local RAG Workshop

A beginner-friendly local Retrieval-Augmented Generation (RAG) application for PDFs and DOCX files, built with Python, Streamlit, and Ollama.

## What this project demonstrates

This workshop app walks through the full local RAG flow:

Document → Extract → Clean → Chunk → Embed → Compare → Retrieve → Context → LLM → Answer

The core teaching concepts are:

- Extracting text from uploaded documents
- Cleaning and chunking the content
- Generating local embeddings
- Measuring semantic relevance with cosine similarity
- Retrieving the most relevant chunks
- Sending only grounded context to a local LLM through Ollama
- Answering without paid services or API keys

## Features

- Upload PDF or DOCX files
- Extract text locally
- Clean and split the content into chunks with overlap
- Generate embeddings locally with Sentence Transformers
- Compare query and chunk vectors using cosine similarity
- Select a local Ollama model automatically: Qwen first, Llama fallback
- Show retrieved sources and similarity scores in the UI
- Generate grounded responses using only the uploaded document context
- Handle no-model, no-connection, and empty-document scenarios gracefully

## Project structure

```text
rag_workshop/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── ollama_client.py
│   ├── model_selector.py
│   └── rag_pipeline.py
├── ui/
│   ├── components.py
│   └── styles.py
├── data/
│   └── uploads/
├── tests/
│   ├── test_chunking.py
│   ├── test_model_selection.py
│   └── test_retrieval.py
└── .venv/
```

## Local setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Ollama and start the service.

4. Install one of the required local models:

```bash
ollama pull qwen2.5
```

Or fall back to:

```bash
ollama pull llama3.2
```

5. Run the app:

```bash
streamlit run app.py
```

## Ollama setup

Install Ollama from: https://ollama.com/download

Then verify the service is running:

```bash
ollama list
```

If the service is not running, start it and check the port:

```bash
ollama serve
```

The app expects Ollama on the default URL:

```text
http://localhost:11434
```

## Model policy

The app checks for installed models at runtime and uses the first available model in this order:

1. Qwen family
2. Llama family
3. If neither is available, show a setup message instead of crashing

## Workshop demonstration

Use any small syllabus, course notes, or policy document. Then ask questions such as:

- What are the eligibility requirements?
- What are the assignment deadlines?
- Which topics are covered in Week 3?
- Where is the grading policy discussed?

The app will:

1. Load and index the uploaded document
2. Retrieve relevant chunks using cosine similarity
3. Show similarity scores and sources
4. Send only the retrieved context to Ollama
5. Generate a grounded answer

## Troubleshooting

### `Ollama not running`

Check:

```bash
ollama list
```

If it fails, start Ollama.

### No model installed

Run:

```bash
ollama pull qwen2.5
```

or:

```bash
ollama pull llama3.2
```

### PDF extraction fails

Some scanned PDFs may contain images rather than searchable text. The app will show a helpful message instead of crashing.

### Empty document or no relevant retrieval

The app avoids sending irrelevant content to the LLM and responds transparently when the answer is not found.

## Why each technology is used

- Streamlit: quick, beginner-friendly UI
- PyMuPDF: fast local PDF extraction
- python-docx: DOCX extraction
- Sentence Transformers: local embeddings without paid APIs
- NumPy + scikit-learn: cosine similarity and vector math
- Ollama: local LLM runtime using Qwen or Llama

## Important concept

RAG is not just “read the document.” The workflow is:

1. Extract text
2. Chunk it into smaller parts
3. Generate embeddings
4. Retrieve relevant chunks by similarity
5. Add them as context to the model
6. Generate a grounded answer

This keeps the response grounded in the uploaded document instead of relying on general model memory.

## Educational note

Documents are untrusted data. The app treats retrieved text as reference context, not system instructions. The system prompt is kept separate from the document content so the document cannot override the model’s safety behavior.
