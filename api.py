from fastapi import FastAPI, Query
import pandas as pd
from engine import load_catalog  # Make sure engine.py properly loads your CSV

app = FastAPI(title="SHL Assessment Recommendation API")

# Load the dataset once when the app starts
df = load_catalog()

@app.get("/")
def home():
    return {
        "message": "Welcome to the SHL Assessment Recommendation API. Use /recommend?query=your_keyword to get suggestions."
    }

@app.get("/recommend")
def recommend(query: str = Query(..., description="Job role, skill, or keyword")):
    # Filter dataset using query
    results = df[
        df['job_roles'].str.contains(query, case=False, na=False) |
        df['skills'].str.contains(query, case=False, na=False) |
        df['assessment_name'].str.contains(query, case=False, na=False)
    ]

    # If no results found
    if results.empty:
        return {"message": "No assessments found for your query."}

    # Return only available fields
    return results[[
        'assessment_name',
        'category',
        'job_roles',
        'skills',
        'level',
        'description'
    ]].to_dict(orient="records")
