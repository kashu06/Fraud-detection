from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import json

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

docs = []
with open("fraud_history.jsonl", "r") as f:
    for line in f:
        txn = json.loads(line)
        text = f"Consumer {txn['consumer_id']} sent ₹{txn['amount']} at {txn['location']} via device {txn['device_id']} at hour {txn['hour']}. Flags: {txn['recent_flags']}"
        docs.append(Document(page_content=text))

Chroma.from_documents(docs, embeddings, persist_directory="chroma_store")
print("ChromaDB initialized ✅")
