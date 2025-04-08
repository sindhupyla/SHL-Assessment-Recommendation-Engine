from fastapi import FastAPI, Query
import pandas as pd
from engine import load_catalog

app = FastAPI()

# Load the catalog
df = load_catalog()

@app.get("/")
def home():
    return {"message": "Welcome to the SHL Assessment API. Use /recommend?query=your_search to get results."}

@app.get("/recommend")
def recommend(query: str = Query(..., description="Search for skill, job role, or keyword")):
    try:
        # Perform case-insensitive search
        results = df[
            df['assessment_name'].str.contains(query, case=False, na=False) |
            df['skills'].str.contains(query, case=False, na=False) |
            df['job_roles'].str.contains(query, case=False, na=False)
        ]

        if results.empty:
            return {"message": "No matching assessments found. Try another keyword."}

        # Return filtered and formatted results
        output = results[[
            "assessment_name",
            "url",
            "remote_testing_support",
            "adaptive_irt_support",
            "duration",
            "test_type"
        ]].head(10)  # Limit to top 10 results

        return output.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
