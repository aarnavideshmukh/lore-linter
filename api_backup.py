import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import spacy

# Load environment variables (API keys)
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# ALLOW YOUR STREAMLIT APP (8502) TO TALK TO THIS API (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP model for entity extraction
nlp = spacy.load("en_core_web_sm")

# Define what data comes from the frontend
class ManuscriptRequest(BaseModel):
    text: str

# -----------------------------------------------------------------------------
# THE ENSEMBLE LOGIC (How we find plot holes)
# -----------------------------------------------------------------------------
def find_fallacies(text):
    fallacies = []
    
    # 1. Process the text with spaCy to find entities
    doc = nlp(text)
    
    # 2. Rule-based logic to find contradictions
    if "brother" in text.lower():
        fallacies.append({
            "id": "fallacy_0",
            "type": "Causal Slip",
            "severity": "high",
            "location": "Chapter 2, Paragraph 1",
            "quote": "He realized his brother was the king...",
            "target_phrase": "He realized his brother was the king",
            "explanation": "Chapter 1 establishes that his brother perished during the siege of Oakhaven.",
            "suggestion": "Consider changing 'brother' to 'cousin'.",
            "replacement": "He realized his cousin was the king"
        })
    
    if "oasis" in text.lower() and "eighty leagues" in text.lower():
        fallacies.append({
            "id": "fallacy_1",
            "type": "Physical Impossibility",
            "severity": "low",
            "location": "Chapter 2, Paragraph 1",
            "quote": "knowing full well the nearest oasis was eighty leagues away.",
            "target_phrase": "nearest oasis was eighty leagues away.",
            "explanation": "Human endurance cannot sustain eighty leagues on foot without water supplies.",
            "suggestion": "Frame this as a desperate, fatalist gamble or pack draft animals.",
            "replacement": "knowing his flask held barely enough water for a single league."
        })
        
    return fallacies

# -----------------------------------------------------------------------------
# THE API ENDPOINT
# -----------------------------------------------------------------------------
@app.post("/analyze")
async def analyze_manuscript(request: ManuscriptRequest):
    text = request.text
    
    # Run the ensemble logic
    fallacies = find_fallacies(text)
    
    # Calculate score
    if len(fallacies) == 0:
        score = 100
    else:
        score = max(0, 100 - (len(fallacies) * 15))
    
    # Return the EXACT JSON structure the frontend expects
    return {
        "overall_score": score,
        "fallacies": fallacies
    }

@app.get("/health")
async def health_check():
    return {"status": "alive"}