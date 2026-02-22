"""
Emotion Diffuser -- Interactive CLI
Run with: python cli.py
"""

import asyncio
import sys
import os

# Ensure the current dir is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from analysis_engine.analyzer import analyze_text

# Try to import mediation (requires OPENAI_API_KEY)
try:
    from mediator_engine.rewrite import rewrite_message_llm, generate_apology_llm
    MEDIATION_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
except ImportError:
    MEDIATION_AVAILABLE = False


RISK_MARKERS = {"high": "[!!!]", "medium": "[!!]", "low": "[ok]"}
RELATIONSHIPS = ["neutral", "parent", "sibling", "friend", "partner", "professional"]


def print_banner():
    print()
    print("=" * 55)
    print("  EMOTION DIFFUSER -- Interactive CLI")
    print("=" * 55)
    print("  Type a message to analyze its emotional content.")
    if MEDIATION_AVAILABLE:
        print("  [+] OpenAI key detected -- rewrites & apologies ON.")
    else:
        print("  [-] No OPENAI_API_KEY -- analysis-only mode.")
        print("      Set it in a .env file to enable rewrites/apologies.")
    print("  Type 'quit' or 'exit' to leave.")
    print()


async def run_analysis(text: str):
    """Analyze a message and display results."""
    print()
    print("  Analyzing...")
    result = await analyze_text(text)

    risk_icon = RISK_MARKERS.get(result.risk, "[?]")
    print()
    print(f"  +-------------------------------------")
    print(f"  | Top Emotion:  {result.emotion.upper()} ({result.intensity:.1%})")
    print(f"  | {risk_icon} Risk Level: {result.risk.upper()}")
    print(f"  | Toxic:        {'YES' if result.is_toxic else 'No'} ({result.toxicity_score:.1%})")
    if result.all_emotions:
        top3 = result.all_emotions[:3]
        breakdown = ", ".join(f"{e.label} {e.score:.0%}" for e in top3)
        print(f"  | Breakdown:    {breakdown}")
    print(f"  +-------------------------------------")

    return result


async def run_mediation(text: str, analysis, relationship: str):
    """Rewrite and generate apology via LLM."""
    print(f"\n  Generating rewrite & apology (tone: {relationship})...")

    rewritten = await rewrite_message_llm(text, analysis, relationship)
    apology_text, components = await generate_apology_llm(text, analysis, relationship)

    print()
    print(f"  +--- CALM REWRITE -------------------")
    print(f"  | {rewritten}")
    print(f"  +-------------------------------------")

    print()
    print(f"  +--- APOLOGY ------------------------")
    print(f"  | {apology_text}")
    if any(components.values()):
        print(f"  |")
        for key, val in components.items():
            if val:
                print(f"  | * {key.title()}: {val}")
    print(f"  +-------------------------------------")


def pick_relationship() -> str:
    """Prompt the user to pick a relationship context."""
    print("\n  Relationship context:")
    for i, r in enumerate(RELATIONSHIPS):
        print(f"    [{i}] {r}")
    choice = input("  Pick (0-5, default 0): ").strip()
    try:
        return RELATIONSHIPS[int(choice)]
    except (ValueError, IndexError):
        return "neutral"


async def main():
    print_banner()

    while True:
        try:
            text = input("  > You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            break

        if not text or text.lower() in ("quit", "exit", "q"):
            print("  Bye!")
            break

        # Step 1: Analysis (always available)
        analysis = await run_analysis(text)

        # Step 2: Mediation (only if API key is available)
        if MEDIATION_AVAILABLE:
            do_mediate = input("\n  Generate rewrite & apology? (y/n, default y): ").strip().lower()
            if do_mediate != "n":
                relationship = pick_relationship()
                try:
                    await run_mediation(text, analysis, relationship)
                except Exception as e:
                    print(f"\n  [ERROR] Mediation failed: {e}")

        print()  # blank line before next prompt


if __name__ == "__main__":
    asyncio.run(main())
