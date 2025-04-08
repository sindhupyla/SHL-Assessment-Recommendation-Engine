import streamlit as st
from engine import load_catalog
import pandas as pd
import datetime

st.set_page_config(page_title="SHL Assessment Engine", layout="wide")
st.title("🧠 SHL Assessment Recommendation Engine")

st.markdown("""
Welcome! Use the filters on the left to find suitable SHL assessments. You can also access the [API here](https://shl-assessment-recommendation-engine.onrender.com/recommend?query=python)
""")

df = load_catalog()

all_roles = sorted(set(r.strip() for roles in df['job_roles'].dropna() for r in roles.split("|")))
all_skills = sorted(set(s.strip() for skills in df['skills'].dropna() for s in skills.split("|")))
all_levels = sorted(df['level'].dropna().unique())
all_categories = sorted(df['category'].dropna().unique())

with st.sidebar:
    st.header("🔍 Filter Criteria")

    selected_roles = st.multiselect("🎯 Job Roles", all_roles)
    selected_skills = st.multiselect("🧠 Key Skills", all_skills)
    selected_levels = st.multiselect("📈 Seniority Level", all_levels, default=["All"])
    selected_categories = st.multiselect("📦 Assessment Category", all_categories)
    search = st.text_input("🔍 Keyword in Assessment Name")

    st.markdown("---")
    st.markdown("""
    ℹ️ **Need the API version?** Try:
    `/recommend?query=communication`
    or
    `/detailed_recommend?query=python`
    """)

def filter_df(df):
    filtered = df.copy()

    if selected_roles:
        filtered = filtered[filtered['job_roles'].apply(
            lambda x: any(role.lower() in x.lower().split("|") for role in selected_roles)
        )]

    if selected_skills:
        for skill in selected_skills:
            filtered = filtered[filtered['skills'].str.contains(skill, case=False, na=False)]

    if selected_levels and "All" not in selected_levels:
        filtered = filtered[filtered['level'].isin(selected_levels + ["All"])]

    if selected_categories:
        filtered = filtered[filtered['category'].isin(selected_categories)]

    if search:
        filtered = filtered[filtered['assessment_name'].str.contains(search, case=False)]

    return filtered.drop_duplicates(subset='assessment_name')

st.markdown("### 📝 Recommended Assessments")

filtered_results = filter_df(df)

filters_applied = any([
    selected_roles,
    selected_skills,
    selected_levels and selected_levels != ["All"],
    selected_categories,
    search
])

if filtered_results.empty:
    if filters_applied:
        st.warning("❗ No perfect matches found based on your filters.")
        st.info("✅ Showing similar assessments:")
        results_to_show = df.sample(10)
    else:
        st.warning("❗ No filters applied. Showing random sample:")
        results_to_show = df.sample(10)
else:
    results_to_show = filtered_results.head(10)
    st.success(f"✅ {len(results_to_show)} assessment(s) shown.")

cols = st.columns(2)
for idx, (_, row) in enumerate(results_to_show.iterrows()):
    col = cols[idx % 2]
    with col:
        st.markdown(f"""
        <div style=\"border:1px solid #DDD; border-radius:12px; padding:16px; margin-bottom:12px; background-color:#FAFAFA; color:#000;\">
        <h4 style=\"color:#000;\"><a href='{row['assessment_url']}' target='_blank'>{row['assessment_name']}</a> <span style=\"font-size:12px; color:#555;\">({row['category']})</span></h4>
        <p><b>Roles:</b> {row['job_roles']}</p>
        <p><b>Skills:</b> {row['skills']}</p>
        <p><b>Level:</b> {row['level']}</p>
        <p><b>Duration:</b> {row['duration']} | <b>Test Type:</b> {row['test_type']}</p>
        <p><b>Remote:</b> {row['remote_testing_support']} | <b>Adaptive:</b> {row['adaptive_irt_support']}</p>
        <p><b>Description:</b> {row['description']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("### 💾 Export Assessments")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
st.download_button(
    label="📥 Download as CSV",
    data=results_to_show.to_csv(index=False),
    file_name=f"recommended_assessments_{timestamp}.csv",
    mime="text/csv"
)

st.markdown("### 💬 Feedback")
feedback = st.text_area("Help us improve this tool!")
if st.button("Submit Feedback"):
    with open("feedback_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}]\n{feedback}\n---\n")
    st.success("Thanks for your feedback!")
