
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

Perfect — this is exactly what judges *love* to see in a repo: clear ownership and modular responsibility.
Below is something you can paste straight into your **README → Team Responsibilities** section.

---

# 👥 Team Responsibilities & File Ownership

To ensure parallel development and minimal merge conflicts, the project is divided into four independent modules.
Each teammate owns a subsystem and its corresponding files.

---

## 🧠 Member 1 — Backend & API Architect

**Role:** System entrypoint, API contracts, request routing
**Skill focus:** FastAPI, JSON design, architecture

### Files owned

```
backend/main.py
backend/routes.py
backend/schemas.py
backend/config.py
```

### Responsibilities

* Define API endpoints (`/analyze`, `/health`, `/rewrite`)
* Define request/response schemas
* Handle validation & error handling
* Load environment variables and settings
* Ensure frontend can communicate with backend

### Deliverable

A working API server that accepts JSON and returns structured responses.

---

## 🔬 Member 2 — Emotion Analysis Engineer

**Role:** Emotion detection + escalation scoring
**Skill focus:** NLP, HuggingFace, Python logic

### Files owned

```
analysis_engine/analyzer.py
analysis_engine/models.py
analysis_engine/utils.py
```

### Responsibilities

* Load emotion & toxicity models
* Implement scoring logic
* Detect escalation triggers
* Output structured emotional analysis

### Deliverable

A function that converts raw text into emotion + risk scores.

---

## 🕊️ Member 3 — AI Mediation Engineer

**Role:** LLM rewriting + tone diffusion
**Skill focus:** LLM APIs, prompt design, output shaping

### Files owned

```
mediator_engine/rewrite.py
mediator_engine/prompts.py
mediator_engine/client.py
```

### Responsibilities

* Write system prompts for tone softening
* Integrate OpenAI/Gemini/Claude APIs
* Handle retries, formatting, token limits
* Produce calm, constructive rewrites

### Deliverable

A function that converts emotional text into a calmer version.

---

## 🎨 Member 4 — Frontend & Integration Engineer

**Role:** User interface + system integration testing
**Skill focus:** Streamlit, UX flow, API calls

### Files owned

```
frontend/app.py
datasets/sample_dialogues.json
tests/test_api.py
tests/test_analysis.py
README.md (demo section)
```

### Responsibilities

* Build user interface for message input/output
* Display emotion analysis visually
* Show rewritten suggestion
* Write demo scripts & test cases
* Prepare demo walkthrough for judges

### Deliverable

A working interface that demonstrates the full pipeline.

---

# 🧩 Shared Responsibility

### `backend/orchestrator.py`

This file is the **integration layer**.

All members collaborate here to connect:

```
analysis_engine → mediator_engine → API output
```

No one edits this file alone — integration happens together near the end.

---

# 🚀 Development Strategy

Each member can work **independently** because:

* API contracts are defined early
* Engines return structured JSON
* Orchestrator connects modules only at final stage

This prevents blocking and enables parallel development.

---

If you want, I can also give you:

👉 a **1-week hackathon timeline**
👉 or a **Git workflow plan so merges don’t explode**

Both massively increase your chances of actually finishing.

Perfect — now we go one level deeper.
Below is **member-by-member actionable instructions**. Not vague roles — actual “open this file → write this kind of code” guidance.

You can paste this into your README under **Implementation Guide**.

---

# 👨‍💻 Member 1 — Backend & API Architect

## `backend/main.py`

You must:

* Create FastAPI app instance
* Register router
* Add title + metadata
* Add root health endpoint

Goal:

```
uvicorn backend.main:app --reload
```

should start the server.

---

## `backend/routes.py`

You must:

* Define POST `/analyze`
* Accept `MessageIn` schema
* Call orchestrator function
* Return JSON response

Do NOT:

* Put ML code here
* Put prompts here

This file only routes requests.

---

## `backend/schemas.py`

You must:

* Define all API input/output formats

Minimum required schemas:

```
MessageIn(text: str)
AnalysisOut(emotion, intensity, risk)
RewriteOut(original, rewritten, emotion)
```

This ensures the whole team speaks the same JSON language.

---

## `backend/config.py`

You must:

* Load environment variables
* Store model names
* Store API keys

Example responsibilities:

```
load OPENAI_API_KEY
set MODEL_NAME
define DEBUG flag
```

This file prevents keys scattered across project.

---

# 🔬 Member 2 — Emotion Analysis Engineer

## `analysis_engine/models.py`

You must:

* Load HuggingFace pipelines
* Cache them globally

Example tasks:

```
emotion_model = pipeline("text-classification", ...)
toxicity_model = pipeline(...)
```

This file only loads models — no logic.

---

## `analysis_engine/utils.py`

You must:

* Write helper logic

Examples:

* keyword triggers
* escalation thresholds
* normalization functions
* scoring adjustments

This file keeps analyzer clean.

---

## `analysis_engine/analyzer.py`

You must:

* Call models
* Interpret outputs
* Combine scores
* Produce structured JSON

Required output format:

```
{
  "emotion": "...",
  "intensity": float,
  "risk": "low/medium/high"
}
```

This file converts raw text → emotional insight.

---

# 🕊️ Member 3 — AI Mediation Engineer

## `mediator_engine/prompts.py`

You must:

* Write all system prompts
* Include few-shot examples
* Define tone rules

Nothing else in project should contain prompts.

This makes prompts editable without touching code.

---

## `mediator_engine/client.py`

You must:

* Implement API wrapper for LLM provider
* Load API key from config
* Handle retries/timeouts
* Return clean string output

This file isolates vendor lock-in.

---

## `mediator_engine/rewrite.py`

You must:

* Accept original text + analysis result
* Build final prompt using prompts.py
* Call client.py
* Return rewritten output

Required output format:

```
{
  "rewritten": "...",
  "tone": "calm"
}
```

This file performs the actual mediation.

---

# 🎨 Member 4 — Frontend & Integration Engineer

## `frontend/app.py`

You must:

* Create text input box
* Send POST request to backend
* Display emotion analysis
* Display rewritten suggestion

Minimum demo flow:

```
User types message → clicks button → sees calm rewrite
```

Use Streamlit for speed.

Run with:

```
streamlit run frontend/app.py
```

---

## `datasets/sample_dialogues.json`

You must:

* Add sample arguments
* Add angry conversations
* Add neutral cases
* Add conflict escalation examples

These will be used for demo/testing.

---

## `tests/test_api.py`

You must:

* Test API endpoint works
* Test JSON schema valid
* Test server response time

Run with:

```
pytest tests/test_api.py
```

---

## `tests/test_analysis.py`

You must:

* Feed sample dialogues to analyzer
* Verify emotion labels reasonable
* Ensure risk scoring consistent

Run with:

```
pytest tests/test_analysis.py
```

---

# 🧩 ALL MEMBERS — Integration Phase

## `backend/orchestrator.py`

This file connects everything.

Final pipeline must be:

```
1. Receive text
2. Call analyzer
3. Call rewrite engine
4. Merge outputs
5. Return final JSON
```

No one writes this fully alone.

This file is built together once modules are ready.

---
