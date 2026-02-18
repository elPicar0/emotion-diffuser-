from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EmotionInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "server running"}


@app.post("/analyze")
def analyze(data: EmotionInput):
    # placeholder logic
    text = data.text.lower()
    
    if "happy" in text:
        emotion = "positive"
    elif "sad" in text:
        emotion = "negative"
    else:
        emotion = "neutral"
    
    return {"emotion": emotion}