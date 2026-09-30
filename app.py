import os
import tempfile

import streamlit as st

from core.model_selector import select_ollama_model
from core.ollama_client import is_ollama_available
from core.rag_pipeline import RAGPipeline
from ui.components import status_badge
from ui.styles import apply_styles

apply_styles()

st.set_page_config(page_title="Local RAG Workshop", page_icon="📚", layout="wide")
st.title("Local RAG Workshop")
st.caption("Upload a PDF or DOCX, retrieve the most relevant chunks, and ask grounded questions using a local Ollama model.")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline(chunk_size=500, overlap=80, top_k=3, min_similarity=0.1)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed_document" not in st.session_state:
    st.session_state.indexed_document = None

sidebar = st.sidebar
sidebar.title("Settings")
st.session_state.pipeline.chunk_size = sidebar.number_input("Chunk size", min_value=200, max_value=1200, value=500, step=50)
st.session_state.pipeline.overlap = sidebar.number_input("Chunk overlap", min_value=20, max_value=300, value=80, step=10)
st.session_state.pipeline.top_k = sidebar.slider("Top-K retrieval", min_value=1, max_value=10, value=3)
st.session_state.pipeline.min_similarity = sidebar.slider("Minimum similarity", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
selected_model = select_ollama_model()
ollama_connected = is_ollama_available()

header_col1, header_col2 = st.columns([2, 1])
with header_col1:
    st.subheader("Model and status")
with header_col2:
    st.caption("Workshop runtime")

st.markdown("#### Status")
status_badge("Connected" if ollama_connected else "Not Connected", ollama_connected)
status_badge(f"Model: {selected_model or 'Unavailable'}", bool(selected_model))

if not selected_model:
    st.warning("No compatible Qwen or Llama model was detected. Install one with `ollama pull qwen2.5` or `ollama pull llama3.2`.")

st.markdown("---")
st.subheader("1. Upload a document")
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file is not None:
    suffix = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    try:
        document_info = st.session_state.pipeline.index_document(temp_path)
        st.session_state.indexed_document = uploaded_file.name
        st.success(f"Indexed {uploaded_file.name} successfully.")
    except Exception as exc:  # pragma: no cover - UI error path
        st.error(str(exc))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    if st.session_state.indexed_document:
        st.markdown("### Document overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='metric-card'><b>Document</b><br>{}</div>".format(st.session_state.indexed_document), unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'><b>Characters</b><br>{}</div>".format(document_info.get("char_count", 0)), unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'><b>Chunks</b><br>{}</div>".format(document_info.get("chunk_count", 0)), unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='metric-card'><b>Pages</b><br>{}</div>".format(document_info.get("page_count", 0)), unsafe_allow_html=True)

st.markdown("---")
st.subheader("2. Chat with the uploaded document")

if st.session_state.indexed_document is None:
    st.info("Upload a document to begin. The app will extract the text, generate chunks, and prepare the knowledge base.")

for item in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(item["question"])
    with st.chat_message("assistant"):
        st.write(item["answer"])

    if item.get("retrieved"):
        with st.expander("View retrieved context"):
            for retrieved in item["retrieved"]:
                st.markdown(
                    f"**{retrieved['chunk_id']}** | Similarity: {retrieved['similarity']} | Source: {retrieved['source']} | Page: {retrieved.get('page', 'n/a')}"
                )
                st.write(retrieved["text"])

if st.session_state.indexed_document is not None:
    prompt = st.chat_input("Ask a question about the uploaded document")
    if prompt:
        response = st.session_state.pipeline.answer_query(
            prompt,
            top_k=st.session_state.pipeline.top_k,
            min_similarity=st.session_state.pipeline.min_similarity,
            model_name=selected_model,
        )
        st.session_state.chat_history.append({
            "question": prompt,
            "answer": response["answer"],
            "retrieved": response.get("retrieved", []),
        })
        st.rerun()

st.markdown("---")
st.subheader("3. Retrieval transparency")

if st.session_state.chat_history:
    latest_retrieval = st.session_state.chat_history[-1].get("retrieved", [])
    if latest_retrieval:
        def row_mapper(item):
            return {
                "Chunk ID": item["chunk_id"],
                "Similarity": item["similarity"],
                "Source": item["source"],
                "Page": item.get("page", "n/a"),
                "Text": item["text"],
            }

        st.dataframe([row_mapper(item) for item in latest_retrieval], use_container_width=True)
    else:
        st.info("No relevant chunks were matched for the most recent question.")
else:
    st.info("The retrieval panel will appear once you ask a question.")

st.markdown("---")
st.subheader("4. Knowledge base status")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Documents", 1 if st.session_state.indexed_document else 0)
with col2:
    st.metric("Chunks", len(st.session_state.pipeline.chunks))
with col3:
    st.metric("Embeddings", "Ready" if st.session_state.pipeline.chunk_vectors.size else "Not ready")
with col4:
    st.metric("Retrieval", "Ready" if st.session_state.pipeline.chunks else "Waiting")

sidebar.markdown("### Ollama model")
if selected_model:
    sidebar.success(f"Selected model: {selected_model}")
else:
    sidebar.warning("No suitable local model is installed. Use `ollama pull qwen2.5` or `ollama pull llama3.2`.")

sidebar.markdown("### Workshop explanation")
sidebar.write("The app first retrieves relevant document chunks using embeddings and cosine similarity, then sends just that context to a local Ollama model for grounded generation.")
