from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import json, os, requests, traceback
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from custom_embeddings import CustomHFEmbeddings
from agent.agent_executor import agent_executor
import os
load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

MODEL_NAME = "deepseek/deepseek-v3-0324"
FRAUD_FILE = "fraud_history.jsonl"

class Transaction(BaseModel):
    consumer_id: str = Field(..., alias="consumerId")
    amount: float
    location: str
    hour: int
    device_id: str = Field(..., alias="deviceId")
    known_locations: list[str] = Field(..., alias="knownLocations")
    known_devices: list[str] = Field(..., alias="knownDevices")
    average_transaction_amount: float = Field(..., alias="averageTransactionAmount")
    recent_flags: list[str] = Field(default=[], alias="recentFlags")

@app.get("/")
def root():
    return {"status": "FastAPI backend is running ✅"}

@app.post("/analyze")
def analyze(txn: Transaction):
    try:
        prompt = f"""
You are an expert fraud analyst.
Analyze this transaction:
{json.dumps(txn.model_dump(by_alias=True), indent=2)}
Return:
1. Risk Score (0–100)
2. Verdict [Likely Fraud / Unusual but Safe / Safe]
3. Explanation
4. Suggested Action
"""
        payload = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]

        verdict = "Review"
        if "Likely Fraud" in answer:
            verdict = "Fraud"
        elif "Safe" in answer:
            verdict = "Safe"

        record = txn.model_dump(by_alias=True)
        record.update({
            "analyzed_at": datetime.utcnow().isoformat(),
            "ai_verdict": verdict,
            "user_feedback": "Pending",
            "final_verdict": verdict
        })

        with open(FRAUD_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")

        return {"analysis": answer, "ai_verdict": verdict}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/log-session")
async def log_session(request: Request):
    try:
        payload = await request.json()
        sid, data = payload["session_id"], payload["data"]
        print(f"📥 Logging session: {sid} with data: {data}")

        os.makedirs("sessions", exist_ok=True)
        with open(f"sessions/{sid}.jsonl", "a") as f:
            f.write(json.dumps({"data": data}) + "\n")

        return {"status": "logged"}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/hijack-check")
async def hijack_check(request: Request):
    try:
        body = await request.body()
        if not body:
            return {"hijack_analysis": "⚠️ Empty body."}

        data = json.loads(body)
        sid = data["session_id"]
        path = f"sessions/{sid}.jsonl"

        if not os.path.exists(path):
            return {"hijack_analysis": "⚠️ No session data found."}

        logs = [json.loads(line)["data"] for line in open(path)][-3:]
        baseline = {
            "typing_interval_ms": 160,
            "timezoneOffset": 330,
            "fingerprint": logs[0].get("fingerprint", "unknown")
        }

        prompt = f"""
Behavior logs:
{json.dumps(logs, indent=2)}

Baseline:
{json.dumps(baseline, indent=2)}

Return:
- Hijack Score (0–100)
- Verdict (Likely Hijack / Unusual but Okay / Safe)
- Explanation
"""
        payload = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}]}
        answer = requests.post(API_URL, headers=HEADERS, json=payload).json()
        return {"hijack_analysis": answer["choices"][0]["message"]["content"]}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/rebuild-chroma")
def rebuild_chroma():
    try:
        docs = []
        for line in open(FRAUD_FILE):
            txn = json.loads(line)
            if txn.get("user_feedback") != "Validated":
                continue
            txt = (
                f"Consumer {txn['consumer_id']} sent ₹{txn['amount']} at {txn['location']} "
                f"via device {txn['device_id']} at hour {txn['hour']}. "
                f"Flags: {', '.join(txn.get('recent_flags', []))}. Verdict: {txn['final_verdict']}"
            )
            docs.append(Document(page_content=txt))

        Chroma.from_documents(
            documents=docs,
            embedding=CustomHFEmbeddings(),
            persist_directory="chroma_store"
        )
        return {"message": f"ChromaDB rebuilt with {len(docs)} validated transactions ✅"}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
