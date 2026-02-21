
import asyncio
import sys
from analysis_engine.analyzer import analyze_text

async def test_real_analysis():
    test_cases = [
        "I am so incredibly angry that you did this without telling me!",
        "I'm feeling a bit down lately, everything seems so difficult.",
        "You're such a brilliant mind, truly one in a million.", # Possible sarcasm check
        "Shut up you absolute idiot!", # Toxicity check
    ]
    
    print("\n=== Real Analysis Engine Test ===")
    for text in test_cases:
        print(f"\nProcessing: '{text}'")
        try:
            result = await analyze_text(text)
            print(f"Top Emotion: {result.emotion} ({result.intensity})")
            print(f"Risk: {result.risk}")
            print(f"Toxic: {result.is_toxic} (score: {result.toxicity_score})")
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_real_analysis())
