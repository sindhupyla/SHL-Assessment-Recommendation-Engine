from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
from engine import load_catalog

app = FastAPI()

df = load_catalog()

@app.get("/")
def home():
    return {"message": "Welcome to the SHL Assessment API. Use /recommend?query=your_query to get assessments."}

@app.get("/recommend")
def recommend(query: str = Query(..., description="Enter job role, skill, or keyword")):
    try:
        # Filter based on query in multiple fields
        results = df[
            df['job_roles'].str.contains(query, case=False, na=False) |
            df['skills'].str.contains(query, case=False, na=False) |
            df['assessment_name'].str.contains(query, case=False, na=False)
        ]

        if results.empty:
            return JSONResponse(content={"results": []}, status_code=200)

        # Limit to 10 results max
        recommendations = []
        for _, row in results.head(10).iterrows():
            recommendations.append({
                "assessment_name": row['assessment_name'],
                "assessment_url": row['assessment_url'],
                "remote_testing_support": row['remote_testing_support'],
                "adaptive_irt_support": row['adaptive_irt_support'],
                "duration": row['duration'],
                "test_type": row['test_type']
            })

        return {"results": recommendations}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
