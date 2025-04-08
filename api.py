from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from engine import load_catalog

app = FastAPI(title="SHL Assessment Recommendation API")

# Allow CORS for browser/front-end requests (just in case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the SHL catalog
df = load_catalog()

@app.get("/")
def root():
    return {"message": "Welcome to the SHL Assessment API. Use /recommend to find assessments."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/recommend")
def recommend(query: str = Query(..., description="Enter job role, skills, or keyword")):
    results = df[
        df['job_roles'].str.contains(query, case=False, na=False) |
        df['skills'].str.contains(query, case=False, na=False) |
        df['assessment_name'].str.contains(query, case=False, na=False)
    ]

    if results.empty:
        return {"results": []}

    results = results.head(10)

    recommendations = []
    for _, row in results.iterrows():
        recommendations.append({
            "assessment_name": row['assessment_name'],
            "assessment_url": row['assessment_url'],
            "remote_testing_support": "Yes" if row['remote_testing_support'] else "No",
            "adaptive_irt_support": "Yes" if row['adaptive_irt_support'] else "No",
            "duration": row['duration'],
            "test_type": row['test_type']
        })

    return {"results": recommendations}

# Only needed locally, not on Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
