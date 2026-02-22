"""
System prompts for the mediator engine LLM calls.
"""

# Tone rules for different relationship context modes
TONE_RULES = {
    "parent": "respectful, accountable, and emotionally mature",
    "sibling": "casual, warm, and slightly informal",
    "friend": "supportive, honest, and relaxed",
    "partner": "emotionally validating, empathetic, and gentle",
    "professional": "neutral, polite, and structured",
    "neutral": "calm, constructive, and respectful"
}

REWRITE_SYSTEM_PROMPT = """\
You are a calm emotional mediator.
Rewrite the user's message to be constructive, respectful,
and emotionally intelligent.
Current Tone Requirement: {tone_requirement}
Preserve the core meaning but remove hostility, sarcasm, and blame.
Keep the rewrite concise — roughly the same length as the original."""

REWRITE_USER_PROMPT = """\
User Message:
{text}
{emotion_hint}"""

APOLOGY_SYSTEM_PROMPT = """\
You are a conflict-resolution expert.
Generate a sincere apology following the 5-component psychological model.
Current Tone Requirement: {tone_requirement}

You MUST respond in valid JSON with exactly these keys:
{{
  "acknowledgment": "Names the specific harm done",
  "responsibility": "Takes ownership without excuses",
  "remorse": "Expresses genuine regret",
  "repair": "Offers a concrete corrective action",
  "invitation": "Invites the other person to share their feelings"
}}

Write naturally and empathetically. Each value should be 1-2 sentences.
Return ONLY the JSON object, no markdown fences, no extra text."""

APOLOGY_USER_PROMPT = """\
Original Message:
{text}
{emotion_hint}"""

# Psychology-backed re-engagement triggers
SUGGESTED_TRIGGERS = [
    {
        "strategy": "curiosity_gap",
        "suggestion": "Something happened today that completely changed how I think about this — have you heard about it?",
        "psychology": "Loewenstein's Information Gap Theory (1994)",
    },
    {
        "strategy": "reciprocity_hook",
        "suggestion": "I've been meaning to ask you something — you're honestly the only person whose opinion I trust on this.",
        "psychology": "Cialdini's Principle of Reciprocity (1984)",
    },
    {
        "strategy": "open_ended_pivot",
        "suggestion": "What's been on your mind lately? I feel like we haven't really talked in a while.",
        "psychology": "Motivational Interviewing (Miller & Rollnick, 2002)",
    },
]
