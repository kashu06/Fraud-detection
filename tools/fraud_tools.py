from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

@tool
def search_similar_cases(query: str) -> str:
    """Searches similar historical fraud cases using ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="chroma_store", embedding_function=embeddings)
    results = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in results])
