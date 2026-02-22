# 🕊️ Emotion Diffuser

**Emotion Diffuser** is a mental-health-focused emotional mediation system designed to reduce digital toxicity and facilitate relationship repair.

## 🚀 Overview
The system acts as an "EQ layer" for digital communication. It analyzes the emotional intent of a message and provides constructive, psychology-backed alternatives to prevent conflict escalation.

### Core Features
*   🕵️‍♂️ **Real-time Emotion Analysis**: Detects 6 primary emotions (anger, joy, sadness, fear, surprise, disgust).
*   ☠️ **Toxicity Detection**: Identifies aggressive language and calculates a combined escalation risk.
*   🕊️ **Context-Aware Mediation**: Personalizes message rewrites based on relationship context (Parent, Friend, Partner, Professional).
*   🧠 **Psychology-Backed Apologies**: Generates sincere, 5-component apologies (Acknowledgment, Responsibility, Remorse, Repair, Invitation).

## 🛠️ Tech Stack
*   **Backend**: FastAPI (Python)
*   **ML Engine**: HuggingFace Transformers (`DistilRoBERTa` for emotions, `ToxicBERT` for toxicity)
*   **LLM Provider**: OpenAI GPT-4 (for rewrites and apologies)
*   **Frontend**: Streamlit (In development)

## 📁 Architecture
Built on a modular "Member-based" architecture as defined in `Creed.md`:
*   `/backend`: API routing, schemas, and orchestration (Member 1)
*   `/analysis_engine`: Real ML inference and scoring logic (Member 2)
*   `/mediator_engine`: LLM prompt design and tone diffusion (Member 3)

## 🏁 Getting Started

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root:
```env
OPENAI_API_KEY=your_key_here
```

### 3. Run the Backend
```bash
python -m uvicorn backend.main:app --reload
```

## 👥 Meet the Team
*   **Member 1**: Backend & AI Architect (Shaun)
*   **Member 2**: Emotion Analysis Engineer
*   **Member 3**: AI Mediation Engineer
*   **Member 4**: Frontend & Integration Engineer
