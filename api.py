from fastapi import FastAPI, Query
import pandas as pd
from engine import load_catalog  # Make sure engine.py properly loads your CSV

app = FastAPI(title="SHL Assessment Recommendation API")

# Load the dataset once when the app starts
df = load_catalog()

@app.get("/")
def home():
    return {
        "message": "Welcome to the SHL Assessment Recommendation API. Use /recommend?query=your_keyword to get suggestions. \n\n"
                   "✅ Sample Query Keywords for Evaluation (based on your dataset):\n\n"
                   "Use: https://shl-assessment-recommendation-engine.onrender.com/recommend?query=<keyword>\n\n"
                   "🔹 From skills:\n"
                   "- communication\n"
                   "- excel\n"
                   "- python\n"
                   "- numerical reasoning\n"
                   "- problem solving\n\n"
                   "🔹 From job_roles:\n"
                   "- data analyst\n"
                   "- software engineer\n"
                   "- sales manager\n"
                   "- project manager\n"
                   "- consultant\n\n"
                   "🔹 From assessment_name:\n"
                   "- verbal reasoning\n"
                   "- numerical test\n"
                   "- cognitive ability\n"
                   "- personality profiler\n"
                   "- language proficiency\n\n"
                   "📎 Example Test URLs:\n"
                   "1. /recommend?query=communication\n"
                   "2. /recommend?query=data%20analyst\n"
                   "3. /recommend?query=numerical%20test\n"
                   "4. /recommend?query=excel\n"
                   "5. /recommend?query=consultant"
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
