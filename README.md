# Fraud Detection AI Agent

Simple AI-based fraud detection backend using FastAPI and Chroma vector database.

## Features
- Detects fraudulent transactions
- Logs sessions and checks for hijacking
- Uses custom embeddings for AI analysis

## Tech Stack
- Python, FastAPI
- Chroma vector DB
- HTML templates for basic UI

## Repo Structure
```
agent/                 # Backend AI logic
tools/                 # UI helpers
main.py                # FastAPI entry point
init_vector_db.py      # Vector DB setup
custom_embeddings.py   # AI embeddings
requirements.txt       # Python dependencies
Dockerfile             # Docker setup
.gitignore
README.md
```

## Installation

### Clone repo
```bash
git clone https://github.com/kashu06/Fraud-detection.git
```

### Enter directory
```bash
cd fraud_detector_agent
```

### Create and activate venv
```bash
python3 -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Setup
Create a `.env` file with:
```env
OPENAI_API_KEY=your_openai_api_key
```

## Initialize Vector Database
```bash
python init_vector_db.py
```

## Run the FastAPI Server
```bash
uvicorn main:app --reload
```

## Usage
- Access dashboard at http://127.0.0.1:8000
- Use API endpoints for real-time fraud detection
- Session logs stored automatically

## Docker Setup (Optional)

### Build Docker image
```bash
docker build -t fraud-agent .
```

### Run container
```bash
docker run -p 8000:8000 --env-file .env fraud-agent
```

Access at http://localhost:8000
