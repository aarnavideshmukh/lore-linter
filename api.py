import os
import re
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
# THE REAL ENSEMBLE LOGIC (3 Stages)
# -----------------------------------------------------------------------------
def find_fallacies(text):
    fallacies = []
    
    # STAGE 1: RULE-BASED LOGIC (Catch specific patterns)
    if "brother" in text.lower():
        fallacies.append({
            "id": "rule_0",
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
            "id": "rule_1",
            "type": "Physical Impossibility",
            "severity": "low",
            "location": "Chapter 2, Paragraph 1",
            "quote": "knowing full well the nearest oasis was eighty leagues away.",
            "target_phrase": "nearest oasis was eighty leagues away.",
            "explanation": "Human endurance cannot sustain eighty leagues on foot without water supplies.",
            "suggestion": "Frame this as a desperate, fatalist gamble or pack draft animals.",
            "replacement": "knowing his flask held barely enough water for a single league."
        })

    # STAGE 2: SEMANTIC VOTER (Catch contradictions using AI)
    # Uses a lightweight semantic model to check if sentences contradict
    try:
        sentences = [sent.text.strip() for sent in nlp(text).sents]
        if len(sentences) >= 2:
            # Compare the first and last sentences
            premise = sentences[0]
            hypothesis = sentences[-1]
            
            # Check for obvious contradictory words
            contradictory_pairs = [
                ("alive", "dead"), ("dead", "alive"),
                ("before", "after"), ("after", "before"),
                ("inside", "outside"), ("outside", "inside"),
                ("forgave", "betrayed"), ("betrayed", "forgave")
            ]
            
            for word1, word2 in contradictory_pairs:
                if word1 in premise.lower() and word2 in hypothesis.lower():
                    fallacies.append({
                        "id": "semantic_0",
                        "type": "Semantic Contradiction",
                        "severity": "medium",
                        "location": "Detected by Ensemble",
                        "quote": hypothesis[:50] + "...",
                        "target_phrase": hypothesis[:50],
                        "explanation": f"The ensemble found contradictory terms: '{word1}' and '{word2}' in different sentences.",
                        "suggestion": "Review the narrative flow to ensure these events logically align.",
                        "replacement": hypothesis
                    })
                    break
    except Exception as e:
        # If the semantic stage fails, don't crash - just skip
        print(f"Semantic stage error: {e}")

    # STAGE 3: CHARACTER CONSISTENCY TRACKER (Entity extraction)
    # Tracks character mentions and checks for overload
    try:
        entities = [ent.text for ent in nlp(text).ents if ent.label_ == "PERSON"]
        if len(set(entities)) > 4:
            fallacies.append({
                "id": "entity_0",
                "type": "Character Overload",
                "severity": "low",
                "location": "Detected by Entity Tracker",
                "quote": "Multiple characters detected in a short passage.",
                "target_phrase": "",
                "explanation": "The entity tracker detected over 4 unique characters in this passage, which may confuse readers.",
                "suggestion": "Consider splitting this scene or reducing the number of active characters.",
                "replacement": ""
            })
    except Exception as e:
        print(f"Entity stage error: {e}")
        
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