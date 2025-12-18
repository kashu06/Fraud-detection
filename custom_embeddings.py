# from langchain_core.embeddings import Embeddings
# from sentence_transformers import SentenceTransformer

# class CustomHFEmbeddings(Embeddings):
#     def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)

#     def embed_documents(self, texts):
#         return self.model.encode(texts, show_progress_bar=False).tolist()

#     def embed_query(self, text):
#         return self.model.encode([text])[0].tolist()
from langchain_core.embeddings import Embeddings
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
import os

class CustomHFEmbeddings(Embeddings):
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.getenv("HUGGINGFACE_API_KEY"),
            model_name=model_name
        )

    def embed_documents(self, texts):
        return self.embedding.embed_documents(texts)

    def embed_query(self, text):
        return self.embedding.embed_query(text)
