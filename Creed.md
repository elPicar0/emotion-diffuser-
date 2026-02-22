
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

* Defines HTTP endpoints (`/analyze`, `/health`, `/feedback`, `/apologize`)
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
ApologyOut
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
text → analyze emotion → check escalation → rewrite → generate apology → return JSON
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

### `rewrite.py` — LLM rewrite + apology logic

**Purpose**

* Takes emotional analysis + original text
* Requests LLM rewrite (tone softening)
* Generates heartfelt apology when escalation is detected
* Returns softened message + apology suggestion

**Output example (rewrite)**

```
{
  "rewritten": "...",
  "tone": "calm"
}
```

**Output example (apology)**

```
{
  "apology": "I realize what I said about ___ was hurtful. I take full responsibility...",
  "tone": "empathetic",
  "repair_type": "acknowledgment + ownership + repair"
}
```

**Used by**

```
orchestrator.py
```

---

### `prompts.py` — prompt definitions ONLY

**Purpose**

* Stores all system prompts (rewrite + apology)
* Stores few-shot examples for tone softening
* Stores few-shot examples for heartfelt apology generation
* Prevents prompt chaos across files

**This file should be the ONLY place containing prompts**

**Used by**

```
rewrite.py (both rewrite() and generate_apology())
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
rewrite.py (rewrite + apology functions)
```

---

# 🔹 frontend/

### `app.py` — Streamlit UI

**Purpose**

* Text input box
* Displays analysis
* Displays rewritten output
* Displays heartfelt apology suggestion
* Calls backend API (`/analyze`, `/apologize`)

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
           ↓                ↓
      calm rewrite    heartfelt apology
           ↓                ↓
         JSON response (merged)
```

**The system doesn't just de-escalate — it helps people repair relationships.**

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

* Define API endpoints (`/analyze`, `/health`, `/rewrite`, `/apologize`)
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
* Write system prompts for heartfelt apology generation
* Integrate OpenAI/Gemini/Claude APIs
* Handle retries, formatting, token limits
* Produce calm, constructive rewrites
* Produce genuine, empathetic apologies that acknowledge + own + repair

### Deliverable

Two functions: one that converts emotional text into a calmer version, and one that generates a heartfelt apology.

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
* Show heartfelt apology suggestion
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
* Define POST `/apologize`
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
ApologyOut(original, apology, tone, repair_type)
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

* Write all system prompts (rewrite + apology)
* Include few-shot examples for tone softening
* Include few-shot examples for heartfelt apologies
* Define tone rules
* Define apology structure: acknowledgment → ownership → repair offer

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

* Implement `rewrite()` — accepts original text + analysis, returns calm rewrite
* Implement `generate_apology()` — accepts original text + analysis, returns heartfelt apology
* Build final prompt using prompts.py
* Call client.py

Required output format (rewrite):

```
{
  "rewritten": "...",
  "tone": "calm"
}
```

Required output format (apology):

```
{
  "apology": "I realize that what I said was hurtful. I take responsibility for...",
  "tone": "empathetic",
  "repair_type": "acknowledgment + ownership + repair"
}
```

This file performs the actual mediation AND relationship repair.

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
User types message → clicks button → sees calm rewrite + heartfelt apology
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
3. Call rewrite engine (tone softening)
4. Call apology engine (heartfelt apology generation)
5. Merge outputs
6. Return final JSON
```

No one writes this fully alone.

This file is built together once modules are ready.

---

# 💛 Core Philosophy: Relationship Repair

This project doesn't just de-escalate conflict — it helps people **repair relationships**.

The heartfelt apology engine is what separates Emotion Diffuser from a simple tone-fixer.

Our apology system follows **established psychological models of apology effectiveness** — not just polite text generation.

---

# 🧠 The 5 Components of a Real Apology (Research-Backed)

## 1️⃣ Acknowledgment of harm

You must show you understand what you did wrong.

❌ "Sorry if you felt hurt."
✅ "I shouldn't have dismissed your idea during the meeting."

**Why it matters:** People want to feel *seen*, not brushed off.

---

## 2️⃣ Taking responsibility

No excuses. No blame shifting.

❌ "I was stressed."
❌ "You misunderstood me."
✅ "That was my mistake."

**Why it matters:** Responsibility signals maturity and trustworthiness.

---

## 3️⃣ Expression of remorse

Show genuine regret.

❌ robotic: "I apologize."
✅ human: "I feel bad about how I handled that."

**Why it matters:** Emotion signals sincerity.

---

## 4️⃣ Repair / corrective intent

What will you do differently?

❌ missing step → apology feels empty
✅ "Next time I'll check with you before making changes."

**Why it matters:** People forgive when they see future change.

---

## 5️⃣ Invitation to respond (optional)

Gives the other person agency.

> "I understand if you're still upset, but I'd like to make this right."

**Why it matters:** Conflict resolution is two-sided.

---

# 🧩 LLM Apology Template

The AI must generate apologies following this structure:

```
1. Name the specific action
2. Accept responsibility
3. Express genuine regret
4. Offer repair / corrective change
5. Invite response (optional)
```

This template is enforced via `mediator_engine/prompts.py`.

---

# 🤖 Example Transformation

### Input

> "I ignored my teammate's message because I was annoyed."

### AI Apology Output

> I realize I ignored your message earlier, and that wasn't fair to you.
> That was my mistake, and I shouldn't have let my frustration affect how I responded.
> I'm sorry for making you feel dismissed.
> I'll make sure to communicate properly even when I'm stressed.
> If you want to talk about it, I'm here.

**That feels human, not robotic.**

---

# 🏆 Hackathon Pitch Angle

You can literally say to judges:

> "Our system follows established psychological models of apology effectiveness rather than just generating polite text."

That sounds **research-driven**, not gimmicky.

---

# 🔄 Conversation Triggers: Re-Engagement System (Research-Backed)

When a conversation dies, relationships drift. Emotion Diffuser doesn't just fix *conflict* — it also fixes *silence*.

The system detects when a conversation is losing momentum and suggests **psychologically-grounded triggers** to re-engage.

---

## 🚨 Disengagement Detection Signals

The analysis engine detects conversational fade-out by looking for:

| Signal | Example | Psychology |
|--------|---------|------------|
| **Short responses** | "ok", "yeah", "cool", "hmm" | Low cognitive investment = low interest |
| **Delayed replies** | Response time increasing | Approach-avoidance motivation (Elliot, 2006) |
| **No questions asked** | All statements, no curiosity | Lack of reciprocal engagement |
| **Flat emotional tone** | No humor, excitement, or warmth | Emotional disengagement (Gottman) |
| **Conversation loops** | Repeating same topic without depth | Topic exhaustion |

When **2+ signals** are detected, the system flags the conversation as **disengaging** and offers re-engagement triggers.

---

## 🧠 5 Re-Engagement Strategies (Psychology-Backed)

### 1️⃣ The Curiosity Gap

**Based on:** Loewenstein's Information Gap Theory (1994)

Create a gap between what someone knows and what they *want* to know.

❌ "How was your day?"
✅ "Something wild happened today — remind me to tell you later."

**Why it works:** The brain craves closure. An open loop compels a response.

---

### 2️⃣ The Reciprocity Hook

**Based on:** Cialdini's Principle of Reciprocity (1984)

Share something personal first — people feel compelled to match your vulnerability.

❌ "What are you thinking about?"
✅ "I've been overthinking something all day… can I get your take?"

**Why it works:** Vulnerability invites vulnerability. Giving first triggers giving back.

---

### 3️⃣ The Self-Disclosure Ladder

**Based on:** Jourard's Self-Disclosure Theory (1971)

Gradually deepen the conversation by sharing something slightly more personal.

❌ Surface: "Nice weather today."
✅ Deeper: "I've been thinking about whether I'm actually happy with how things are going."

**Why it works:** Relationships deepen through progressive self-disclosure. Staying surface-level kills connection.

---

### 4️⃣ The Open-Ended Pivot

**Based on:** Motivational Interviewing (Miller & Rollnick, 2002)

Replace closed questions with open ones that invite storytelling.

❌ "Did you like the movie?" → "yeah"
✅ "What part of the movie stuck with you?" → actual conversation

**Why it works:** Open questions activate narrative thinking, which produces longer, richer responses.

---

### 5️⃣ The Validation Anchor

**Based on:** Emotional Validation Theory (Linehan, 1993)

Acknowledge what someone just said before pivoting.

❌ Ignoring their last message and changing topic
✅ "That makes total sense — and it reminds me of something…"

**Why it works:** People disengage when they feel unheard. Validation reopens the door.

---

## 🧩 Trigger Detection Output Format

```
{
  "engagement_level": "low",
  "signals_detected": ["short_responses", "no_questions"],
  "suggested_trigger": {
    "strategy": "curiosity_gap",
    "suggestion": "Something came up today that I think you'd find interesting...",
    "psychology": "Loewenstein's Information Gap Theory"
  }
}
```

This is produced by `analysis_engine/analyzer.py` and surfaced via `orchestrator.py`.

---

## 🤖 Example Transformation

### Input (dying conversation)

```
Person A: "Hey"
Person B: "Hey"
Person A: "What's up"
Person B: "Nothing much"
Person A: "Cool"
```

### System Detection

> ⚠️ Engagement level: LOW — short responses, no questions, flat tone

### Suggested Trigger (Curiosity Gap)

> "I just found out something about [shared interest] that completely changed how I think about it — have you heard about this?"

### Suggested Trigger (Reciprocity Hook)

> "I've been meaning to ask you something — you're honestly the only person whose opinion I trust on this."

---

## 🏗️ Pipeline Integration

```
1. Receive conversation history
2. Analyze engagement signals (analyzer.py)
3. If engagement = low → generate re-engagement trigger
4. Select strategy based on conversation context
5. Return trigger suggestion via /triggers endpoint
```

**New endpoint:** `POST /triggers`
**New schema:** `TriggerOut(engagement_level, signals_detected, suggested_trigger)`

---

> **This is the heart of the project. De-escalation saves the moment. Apologies save the relationship. Triggers keep it alive.**

---

# 👨‍👩‍👧‍👦 Relationship Modes: Context-Aware Mediation

Every relationship has its own rules. What works in an apology to your partner will feel strange to your boss. What re-engages a sibling will annoy a friend.

Emotion Diffuser adapts its **tone, apology structure, and trigger strategy** based on the relationship context.

---

## Why Modes Matter (Psychology)

| Relationship | Power Dynamic | Conflict Style | Attachment Pattern |
|---|---|---|---|
| **Parent** | Asymmetric (they raised you) | Guilt-driven, respect-heavy | Deep obligation, unconditional love |
| **Sibling** | Peer, shared history | Rivalrous, fast-cycling | "Love-hate" bond, quick forgiveness |
| **Partner** | Equal, emotionally vulnerable | High-stakes, attachment-triggered | Gottman's Four Horsemen risk |
| **Friend** | Equal, voluntary | Withdrawal-based, ghosting risk | Low obligation, high optionality |
| **Professional** | Power gap / hierarchy | Formal, reputation-aware | Low intimacy, high consequence |

The system **must not** produce a single generic tone. The `relationship` field in `MessageIn` drives everything downstream.

---

## 🧡 Mode: Parent

**Dynamics:** Parents often feel disrespected; children feel unheard. Conflicts revolve around autonomy vs. care.

**Tone rule:** Respectful, accountable, emotionally mature

**Apology style:**
- Acknowledge their care even when disagreeing
- Show maturity ("I understand where you're coming from")
- Avoid sounding defensive or dismissive

**Rewrite style:**
- Remove eye-rolling tone, sarcasm, "whatever" energy
- Keep the core message but frame it respectfully

**Re-engagement:**
- Lead with gratitude ("I was thinking about what you said earlier…")
- Use questions that show respect for their experience

**Example:**

> ❌ "You never listen to me. You just lecture."
> ✅ "I feel like sometimes when I share something, it turns into advice before I've finished. Can we try just talking?"

---

## 👫 Mode: Sibling

**Dynamics:** Siblings fight fast and make up fast. Humor is the repair tool. There's deep history and little formality.

**Tone rule:** Casual, warm, slightly informal

**Apology style:**
- Keep it light but real
- Humor is okay if sincere
- Avoid over-dramatizing — siblings detect fakeness instantly

**Rewrite style:**
- Soften the edge but keep the personality
- Preserve casual language, don't make it stiff

**Re-engagement:**
- Inside jokes, shared memories work best
- "Remember when…" is the strongest sibling re-engagement hook

**Example:**

> ❌ "You're the most annoying person alive I swear to god"
> ✅ "You drive me crazy sometimes but you know I don't mean it like that. My bad."

---

## 💕 Mode: Partner

**Dynamics:** Most emotionally charged. Gottman's research shows contempt, criticism, defensiveness, and stonewalling destroy relationships. The system must actively counter all four.

**Tone rule:** Emotionally validating, empathetic, gentle

**Apology style:**
- Must validate their feelings FIRST before explaining
- Use "I feel" not "You always"
- Show emotional investment, not just logical repair
- Reference the relationship's value ("I care about us")

**Rewrite style:**
- Remove blame language, absolute words ("always", "never")
- Add emotional validation ("I understand this matters to you")
- Keep vulnerability — partners need to see your feelings, not just your logic

**Re-engagement:**
- Emotional check-ins ("How are you really feeling about us?")
- Shared future references ("I was thinking about that trip we talked about…")
- Physical / quality time suggestions

**Example:**

> ❌ "You never make time for me. I'm done trying."
> ✅ "I've been feeling disconnected lately and I miss how close we used to be. Can we talk about it?"

**Gottman counter-patterns enforced:**

| Horseman | System Response |
|---|---|
| Criticism | Rewrite as specific complaint with "I feel" |
| Contempt | Remove sarcasm/mockery, add appreciation |
| Defensiveness | Add ownership, remove counter-attacks |
| Stonewalling | Suggest taking a break + re-engaging later |

---

## 🫂 Mode: Friend

**Dynamics:** Friendships are voluntary — people can just walk away. Conflicts often end in ghosting rather than confrontation. Apologies must be genuine without being heavy.

**Tone rule:** Supportive, honest, relaxed

**Apology style:**
- Keep it real, not performative
- Acknowledge the friendship's value casually
- Don't over-apologize — friends find that awkward

**Rewrite style:**
- Keep the casual energy but remove sharpness
- Preserve personality and honesty

**Re-engagement:**
- Shared interests and plans work best
- Don't force deep conversations — reignite through activity
- "Bro you need to see this" > "We need to talk"

**Example:**

> ❌ "You ditched me for them, that's messed up"
> ✅ "Ngl that kinda stung when you bailed but it's cool, just lmk next time yeah?"

---

## 💼 Mode: Professional

**Dynamics:** Power dynamics are real. Emotional expression is limited. Everything is reputation-aware. Written records exist.

**Tone rule:** Neutral, polite, structured

**Apology style:**
- Formal acknowledgment + corrective action
- No emotional vulnerability — keep it about impact and solution
- Reference professional standards and expectations

**Rewrite style:**
- Remove ALL emotional language
- Frame everything as constructive feedback
- Use "moving forward" and "I'd like to suggest" language

**Re-engagement:**
- Agenda-based ("I wanted to follow up on…")
- Value-driven ("I have an idea that could help the project")
- Never emotionally pressure a colleague

**Example:**

> ❌ "This meeting was a waste of everyone's time"
> ✅ "I think we could structure our meetings more effectively. Would it help to share an agenda beforehand?"

---

## 🗂️ Implementation Guide

### Where modes are enforced

| File | Role |
|---|---|
| `backend/schemas.py` | `MessageIn.relationship` field carries the mode |
| `mediator_engine/prompts.py` | `TONE_RULES` dict maps mode → tone description |
| `mediator_engine/rewrite.py` | Injects tone requirement into LLM system prompt |
| `backend/orchestrator.py` | Passes `relationship` through the full pipeline |

### Future extensions

Each mode can eventually have:
- Custom few-shot examples in `prompts.py`
- Mode-specific trigger strategies in `SUGGESTED_TRIGGERS`
- Mode-specific apology templates (partner apologies need more emotional depth, professional apologies need action items)
- Cultural sensitivity layers (different cultures have different parent-child dynamics)

### Adding a new mode

1. Add the mode name to `TONE_RULES` in `prompts.py`
2. Add few-shot examples for the mode
3. Add mode-specific trigger strategies to `SUGGESTED_TRIGGERS`
4. Update `schemas.py` docs to list the new mode
5. Update this Creed section with the mode's dynamics

---

> **Relationships aren't one-size-fits-all. Neither should emotional AI be.**

---
