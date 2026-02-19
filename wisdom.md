
---

# 📚 Wisdom — Models, Datasets & ML Resources

A curated list of every model and dataset relevant to Emotion Diffuser.

---

# 🔬 Emotion Detection Models

| Model | What it does | Link |
|-------|-------------|------|
| **j-hartmann/emotion-english-distilroberta-base** | 6 emotions (anger, joy, sadness, fear, surprise, disgust) — most popular | [HuggingFace](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) |
| **SamLowe/roberta-base-go_emotions** | 28 fine-grained emotions — great for nuanced analysis | [HuggingFace](https://huggingface.co/SamLowe/roberta-base-go_emotions) |
| **arpanghoshal/EmoRoBERTa** | 28 emotion categories, RoBERTa-based | [HuggingFace](https://huggingface.co/arpanghoshal/EmoRoBERTa) |
| **cirimus/modernbert-base-emotions** | 7 emotional states, modern architecture | [HuggingFace](https://huggingface.co/cirimus/modernbert-base-emotions) |
| **cardiffnlp/twitter-roberta-base-sentiment** | Positive/negative/neutral sentiment | [HuggingFace](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) |
| **Panda0116/emotion-classification-model** | 6 emotions, ~93% accuracy, DistilBERT | [HuggingFace](https://huggingface.co/Panda0116/emotion-classification-model) |

---

# ☠️ Toxicity / Aggression Detection Models

| Model | What it does | Link |
|-------|-------------|------|
| **unitary/toxic-bert** | General toxicity classification | [HuggingFace](https://huggingface.co/unitary/toxic-bert) |
| **martin-ha/toxic-comment-model** | Toxic comment detection (DistilBERT) | [HuggingFace](https://huggingface.co/martin-ha/toxic-comment-model) |
| **Falconsai/offensive_speech_detection** | Offensive/hate speech detection | [HuggingFace](https://huggingface.co/Falconsai/offensive_speech_detection) |
| **KoalaAI/OffensiveSpeechDetector** | Offensive language in social contexts (DeBERTa) | [HuggingFace](https://huggingface.co/KoalaAI/OffensiveSpeechDetector) |
| **AssistantsLab/Tiny-Toxic-Detector** | Lightweight (2M params) — fast for real-time use | [HuggingFace](https://huggingface.co/AssistantsLab/Tiny-Toxic-Detector) |
| **textdetox/xlmr-large-toxicity-classifier** | Multilingual toxicity (9 languages) | [HuggingFace](https://huggingface.co/textdetox/xlmr-large-toxicity-classifier) |

---

# 📊 Datasets — Emotion & Conversation

| Dataset | What it's for | Size | Link |
|---------|-------------|------|------|
| **dair-ai/emotion** | 6-emotion Twitter dataset (anger, joy, sadness, fear, love, surprise) | ~20K | [HuggingFace](https://huggingface.co/datasets/dair-ai/emotion) |
| **google-research-datasets/go_emotions** | 28 fine-grained emotions from Reddit | 58K | [HuggingFace](https://huggingface.co/datasets/google-research-datasets/go_emotions) |
| **boltuix/emotions-dataset** | 13 distinct emotions | 131K+ | [HuggingFace](https://huggingface.co/datasets/boltuix/emotions-dataset) |
| **facebook/empathetic_dialogues** | 25K empathetic conversations — **perfect for apology engine** | 25K | [HuggingFace](https://huggingface.co/datasets/facebook/empathetic_dialogues) |
| **Svenni551/conversation-emotion-dataset** | Conversation + emotion labels combined | Varies | [HuggingFace](https://huggingface.co/datasets/Svenni551/conversation-emotion-dataset) |

---

# 🕊️ Conflict Resolution & Relationship Repair Datasets

| Dataset | What it's for | Link |
|---------|-------------|------|
| **ClarusC64/instruction_conflict_resolution_v01** | Conflict resolution instruction data | [HuggingFace](https://huggingface.co/datasets/ClarusC64/instruction_conflict_resolution_v01) |
| **anirudh2403/therapy-conversation-synthetic** | Synthetic therapy convos about relationship problems | [HuggingFace](https://huggingface.co/datasets/anirudh2403/therapy-conversation-synthetic) |
| **LuangMV97/Empathetic_counseling_Dataset** | Empathetic counseling dialogues | [HuggingFace](https://huggingface.co/datasets/LuangMV97/Empathetic_counseling_Dataset) |
| **Amod/mental_health_counseling_conversations** | Mental health counseling with relationship dynamics | [HuggingFace](https://huggingface.co/datasets/Amod/mental_health_counseling_conversations) |
| **mattwesney/CoT_Heartbreak_and_Breakups** | Communication breakdown & conflict resolution themes | [HuggingFace](https://huggingface.co/datasets/mattwesney/CoT_Heartbreak_and_Breakups) |

---

# 🎯 Recommended Stack for Emotion Diffuser

### Must-Have (Start with these)

| Purpose | Model/Dataset | Why |
|---------|--------------|-----|
| Emotion detection | `j-hartmann/emotion-english-distilroberta-base` | Fast, accurate, 6 core emotions |
| Toxicity detection | `martin-ha/toxic-comment-model` | Lightweight, reliable escalation detection |
| Training data | `facebook/empathetic_dialogues` | 25K conversations for apology + rewrite training |

### Nice-to-Have (if time permits)

| Purpose | Model/Dataset | Why |
|---------|--------------|-----|
| Granular emotions | `SamLowe/roberta-base-go_emotions` | 28 emotions — judges love granularity |
| Real-time toxicity | `AssistantsLab/Tiny-Toxic-Detector` | 2M params — blazing fast |
| Conflict resolution data | `ClarusC64/instruction_conflict_resolution_v01` | Direct conflict resolution training data |
| Therapy convos | `anirudh2403/therapy-conversation-synthetic` | Relationship repair patterns |

---

# 🔧 Quick Usage Examples

### Emotion Detection

```python
from transformers import pipeline

emotion_pipe = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

result = emotion_pipe("I can't believe you said that to me!")
# → [{'label': 'anger', 'score': 0.87}, {'label': 'sadness', 'score': 0.08}, ...]
```

### Toxicity Detection

```python
from transformers import pipeline

toxicity_pipe = pipeline(
    "text-classification",
    model="martin-ha/toxic-comment-model"
)

result = toxicity_pipe("You're such an idiot!")
# → [{'label': 'toxic', 'score': 0.95}]
```

### Loading Empathetic Dialogues Dataset

```python
from datasets import load_dataset

dataset = load_dataset("facebook/empathetic_dialogues")
print(dataset["train"][0])
# → {'conv_id': '...', 'utterance': '...', 'context': 'proud', ...}
```

---

# 📝 Notes

- All models are available via HuggingFace `transformers` library
- Use `pipeline()` for quick inference
- Cache models globally in `analysis_engine/models.py` to avoid reloading
- Datasets can be loaded with `datasets` library: `pip install datasets`

---
