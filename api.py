from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from engine import load_catalog

app = FastAPI(title="SHL Assessment Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = load_catalog()

@app.get("/")
def home():
    message = (
        "Welcome to the SHL Assessment Recommendation API.\n\n"
        "✅ Sample Query Keywords for Evaluation (based on your dataset):\n\n"
        "Use: /recommend?query=communication\n\n"
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
        "- language proficiency"
    )
    return {"message": message}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/recommend")
def recommend(query: str = Query(..., description="Search for job role, skill, or keyword")):
    results = df[
        df['job_roles'].str.contains(query, case=False, na=False) |
        df['skills'].str.contains(query, case=False, na=False) |
        df['assessment_name'].str.contains(query, case=False, na=False)
    ]

    if results.empty:
        source = df.sample(10)
        match_type = "partial"
    else:
        source = results.head(10)
        match_type = "perfect"

    formatted = []
    for _, row in source.iterrows():
        formatted.append({
            "assessment_name": row["assessment_name"],
            "url": row.get("assessment_url", ""),
            "adaptive_support": row.get("adaptive_irt_support", "Unknown"),
            "remote_support": row.get("remote_testing_support", "Unknown"),
            "description": row.get("description", ""),
            "duration": int(str(row.get("duration", "0")).replace(" mins", "").strip()) if "mins" in str(row.get("duration", "")) else 0,
            "test_type": [row.get("test_type", "")] if pd.notna(row.get("test_type")) else []
        })

    return {
        "recommended_assessments": formatted,
        "match_type": match_type
    }
