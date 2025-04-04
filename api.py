from fastapi import FastAPI, Query
import pandas as pd
from engine import load_catalog

app = FastAPI()

df = load_catalog()

@app.get("/")
def home():
    return {"message": "Welcome to the SHL Assessment API. Use /search to find assessments."}

@app.get("/search")
def search_assessments(query: str = Query(..., description="Enter job role, skill, or keyword")):
    results = df[
        df['job_roles'].str.contains(query, case=False, na=False) |
        df['skills'].str.contains(query, case=False, na=False) |
        df['assessment_name'].str.contains(query, case=False, na=False)
    ]
    
    if results.empty:
        return {"message": "No matching assessments found. Try another keyword!"}
    
    return results.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
