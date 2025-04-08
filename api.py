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
        # fallback to random suggestions
        fallback = df.sample(10)[[
            "assessment_name", "category", "job_roles", "skills", "level", "description"
        ]]
        return {
            "results": fallback.to_dict(orient="records"),
            "match_type": "partial",
            "message": "No exact matches found. Showing fallback suggestions."
        }

    output = results[[
        "assessment_name", "category", "job_roles", "skills", "level", "description"
    ]].head(10)

    return {
        "results": output.to_dict(orient="records"),
        "match_type": "perfect"
    }

@app.get("/detailed_recommend")
def detailed_recommend(query: str = Query(..., description="Search with detailed response format")):
    results = df[
        df['job_roles'].str.contains(query, case=False, na=False) |
        df['skills'].str.contains(query, case=False, na=False) |
        df['assessment_name'].str.contains(query, case=False, na=False)
    ]

    if results.empty:
        fallback = df.sample(10)[[
            "assessment_name", "assessment_url", "remote_testing_support",
            "adaptive_irt_support", "duration", "test_type"
        ]]
        return {
            "results": fallback.to_dict(orient="records"),
            "match_type": "partial",
            "message": "No exact matches found. Showing fallback suggestions."
        }

    output = results[[
        "assessment_name", "assessment_url", "remote_testing_support",
        "adaptive_irt_support", "duration", "test_type"
    ]].head(10)

    return {
        "results": output.to_dict(orient="records"),
        "match_type": "perfect"
    }
