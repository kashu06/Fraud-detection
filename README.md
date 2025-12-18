Fraud Detection AI Agent
Simple AI-based fraud detection backend using FastAPI and Chroma vector database.

Features
Detects fraudulent transactions
Logs sessions and checks for hijacking
Uses custom embeddings for AI analysis
Tech Stack
Python, FastAPI
Chroma vector DB
HTML templates for basic UI
Repo Structure
agent/ # Backend AI logic tools/ # UI helpers main.py # FastAPI entry point init_vector_db.py # Vector DB setup custom_embeddings.py # AI embeddings requirements.txt # Python dependencies Dockerfile # Docker setup .gitignore README.md

bash Copy code

Installation
Clone repo: git clone https://github.com/kashu06/Fraud-detection.git
Enter directory: cd fraud_detector_agent
Create and activate venv:
python3 -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows
Install dependencies: pip install -r requirements.txt

Create .env file with:

env Copy code OPENAI_API_KEY=your_openai_api_key Initialize vector database:

bash Copy code python init_vector_db.py Run the FastAPI server:

bash Copy code uvicorn main:app --reload Usage Access dashboard at http://127.0.0.1:8000

Use API endpoints for real-time fraud detection

Session logs stored automatically

Docker Setup (Optional) Build Docker image:

bash Copy code docker build -t fraud-agent . Run container:

bash Copy code docker run -p 8000:8000 --env-file .env fraud-agent Access at http://localhost:8000t
