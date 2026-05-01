import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "LLM_Deep_Interview_Guide.pdf"
FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_and_split_documents(pdf_path=PDF_PATH):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return text_splitter.split_documents(documents)


def build_and_save_vector_store(pdf_path=PDF_PATH, index_path=FAISS_INDEX_PATH):
    docs = load_and_split_documents(pdf_path)
    db = FAISS.from_documents(docs, get_embeddings())
    db.save_local(index_path)
    return db


def load_vector_store(index_path=FAISS_INDEX_PATH):
    if not os.path.exists(index_path):
        raise FileNotFoundError(
            f"FAISS index not found at '{index_path}'. "
            "Run `python store.py` first to create embeddings."
        )

    return FAISS.load_local(
        index_path,
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def main():
    build_and_save_vector_store()
    print(f"Embeddings created and saved to '{FAISS_INDEX_PATH}'.")


if __name__ == "__main__":
    main()
