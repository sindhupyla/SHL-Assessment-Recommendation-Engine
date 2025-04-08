import pandas as pd

def load_catalog(path="shl_full_catalog.csv"):
    return pd.read_csv(path)

def recommend_assessments(df, job_roles=None, skills=None, levels=None, categories=None, search=None):
    filtered = df.copy()

    if job_roles:
        filtered = filtered[filtered['job_roles'].apply(
            lambda x: any(role.lower() in x.lower().split("|") for role in job_roles)
        )]

    if skills:
        for skill in skills:
            filtered = filtered[filtered['skills'].str.contains(skill, case=False, na=False)]

    if levels and "All" not in levels:
        filtered = filtered[filtered['level'].isin(levels + ["All"])]

    if categories:
        filtered = filtered[filtered['category'].isin(categories)]

    if search:
        filtered = filtered[filtered['assessment_name'].str.contains(search, case=False)]

    return filtered.drop_duplicates(subset='assessment_name')
