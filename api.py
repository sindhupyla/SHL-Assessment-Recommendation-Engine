from fastapi import FastAPI, Query
import pandas as pd

# Create app instance
app = FastAPI()

# Load your dataset
df = pd.read_csv("shl_catalog.csv")

@app.get("/")
def home():
    return {"message": "Welcome to the SHL Assessment API. Use /recommend?query= to search."}

@app.get("/recommend")
def recommend(query: str = Query(..., description="Search for skill, job role, or keyword")):
    try:
        results = df[
            df['assessment_name'].str.contains(query, case=False, na=False) |
            df['skills'].str.contains(query, case=False, na=False) |
            df['job_roles'].str.contains(query, case=False, na=False)
        ]

        if results.empty:
            return {"message": "No matching assessments found. Try another keyword."}

        output = results[[
            "assessment_name",
            "url",
            "remote_testing_support",
            "adaptive_irt_support",
            "duration",
            "test_type"
        ]].head(10)

        return output.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
