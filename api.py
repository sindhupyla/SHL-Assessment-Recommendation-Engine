from fastapi import FastAPI, Query
from typing import List, Optional
import pandas as pd
from engine import load_catalog

app = FastAPI(title="SHL Assessment API")

df = load_catalog()

def filter_df(df, job_role=None, skills=None, level=None, category=None, search=None):
    filtered = df.copy()

    if job_role:
        filtered = filtered[filtered['job_roles'].str.contains(job_role, case=False, na=False)]

    if skills:
        for skill in skills:
            filtered = filtered[filtered['skills'].str.contains(skill, case=False, na=False)]

    if level and level != "All":
        filtered = filtered[filtered['level'].isin([level, "All"])]

    if category:
        filtered = filtered[filtered['category'].str.contains(category, case=False, na=False)]

    if search:
        filtered = filtered[filtered['assessment_name'].str.contains(search, case=False, na=False)]

    return filtered.drop_duplicates(subset='assessment_name')

@app.get("/recommendations")
def get_recommendations(
    job_role: Optional[str] = None,
    skills: Optional[List[str]] = Query(None),
    level: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    results = filter_df(df, job_role, skills, level, category, search)
    return results.to_dict(orient="records")
