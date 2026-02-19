
---

# 📁 Project Architecture Documentation

## 🔹 backend/

### `main.py` — FastAPI entry point

**Purpose**

* Starts the API server
* Registers routes
* Defines global middleware later (CORS, logging, auth)

**Used by**

```
uvicorn backend.main:app --reload
```

---

### `routes.py` — API endpoints

**Purpose**

* Defines HTTP endpoints (`/analyze`, `/health`, `/feedback`)
* Converts JSON → Pydantic schema
* Calls orchestrator

**Never contains**

* ML logic
* prompt logic
* business rules

**Called automatically by**

```
backend.main
```

---

### `schemas.py` — JSON contracts

**Purpose**

* Defines input/output structures
* Ensures frontend/backend compatibility
* Enables FastAPI auto docs

**Example**

```
MessageIn
AnalysisOut
RewriteOut
```

**Used by**

```
routes.py
tests/
frontend/
```

---

### `orchestrator.py` — system brain

**Purpose**

* Connects analysis engine + mediator engine
* Handles pipeline flow:

```
text → analyze emotion → check escalation → rewrite → return JSON
```

**This file controls the logic order of the system**

**Called by**

```
routes.py
```

---

### `config.py` — environment & settings

**Purpose**

* Loads API keys
* Stores model names
* Controls debug flags

**Typical contents**

```
OPENAI_API_KEY
MODEL_NAME
THRESHOLDS
```

**Loaded by**

```
mediator_engine/client.py
analysis_engine/models.py
```

---

# 🔹 analysis_engine/

### `analyzer.py` — emotion + escalation logic

**Purpose**

* Detect emotions
* Detect toxicity / aggression
* Score escalation level
* Return structured result

**Output example**

```
{
  "emotion": "anger",
  "intensity": 0.82,
  "risk": "high"
}
```

**Used by**

```
orchestrator.py
```

---

### `models.py` — model loading layer

**Purpose**

* Loads HuggingFace models
* Caches them for performance
* Abstracts model initialization

**Example responsibilities**

```
load_emotion_model()
load_toxicity_model()
```

**Used by**

```
analyzer.py
```

---

### `utils.py` — helper logic

**Purpose**

* Keyword triggers
* scoring normalization
* escalation thresholds
* text preprocessing

**Used by**

```
analyzer.py
```

---

# 🔹 mediator_engine/

### `rewrite.py` — LLM rewrite logic

**Purpose**

* Takes emotional analysis + original text
* Requests LLM rewrite
* Returns softened message

**Output example**

```
{
  "rewritten": "...",
  "tone": "calm"
}
```

**Used by**

```
orchestrator.py
```

---

### `prompts.py` — prompt definitions ONLY

**Purpose**

* Stores all system prompts
* Stores few-shot examples
* Prevents prompt chaos across files

**This file should be the ONLY place containing prompts**

**Used by**

```
rewrite.py
```

---

### `client.py` — API wrapper

**Purpose**

* Handles OpenAI / Gemini / Claude calls
* Handles retries
* Handles rate limits
* Abstracts vendor switching

**Used by**

```
rewrite.py
```

---

# 🔹 frontend/

### `app.py` — Streamlit UI

**Purpose**

* Text input box
* Displays analysis
* Displays rewritten output
* Calls backend API

**Run with**

```
streamlit run frontend/app.py
```

---

# 🔹 datasets/

### `sample_dialogues.json`

**Purpose**

* Test conversations
* Demo inputs
* Fallback offline dataset

**Used by**

```
tests/
frontend demo mode
analysis benchmarking
```

---

# 🔹 tests/

### `test_analysis.py`

**Purpose**

* Tests emotion detection accuracy
* Ensures scoring consistency
* Prevents regression bugs

**Run with**

```
pytest tests/test_analysis.py
```

---

### `test_api.py`

**Purpose**

* Tests endpoints
* Ensures JSON format validity
* Ensures orchestrator works

**Run with**

```
pytest tests/test_api.py
```

---

# 🔹 Root files

### `requirements.txt`

**Purpose**

* Python dependencies
* Used for deployment

**Install with**

```
pip install -r requirements.txt
```

---

### `README.md`

**Purpose**

* Project explanation
* Setup instructions
* Architecture overview
* Demo instructions

---

# 🧠 How everything flows together

```
Frontend → routes.py → orchestrator.py
           ↓
      analyzer.py → models.py → utils.py
           ↓
      rewrite.py → prompts.py → client.py
           ↓
         JSON response
```

That’s your entire system lifecycle.

---
