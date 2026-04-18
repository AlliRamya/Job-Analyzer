import streamlit as st
import requests
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📊 Job Market Analyzer")

# -----------------------------
# FETCH DATA FROM API
# -----------------------------
@st.cache_data
def load_data():
    url = "https://remoteok.com/api"
    response = requests.get(url)
    data = response.json()

    jobs = []

    for job in data[1:]:
        jobs.append({
            "Title": job.get("position"),
            "Company": job.get("company"),
            "Location": job.get("location"),
            "Skills": ", ".join(job.get("tags", []))
        })

    df = pd.DataFrame(jobs)
    df.dropna(inplace=True)
    df["Skills"] = df["Skills"].str.lower()

    return df

df = load_data()

# -----------------------------
# SHOW DATA
# -----------------------------
st.subheader("📄 Job Listings")
st.dataframe(df.head(50))

# -----------------------------
# FILTER SECTION
# -----------------------------
st.sidebar.header("🔍 Filters")

search_role = st.sidebar.text_input("Search Job Role")

if search_role:
    df = df[df["Title"].str.contains(search_role, case=False)]

# -----------------------------
# TOP SKILLS ANALYSIS
# -----------------------------
st.subheader("🔥 Top Skills in Demand")

all_skills = []

for skills in df["Skills"]:
    all_skills.extend(skills.split(", "))

skill_count = Counter(all_skills)
top_skills = skill_count.most_common(10)

skills, counts = zip(*top_skills)

fig, ax = plt.subplots()
ax.bar(skills, counts)
plt.xticks(rotation=45)

st.pyplot(fig)

# -----------------------------
# LOCATION ANALYSIS
# -----------------------------
st.subheader("🌍 Job Locations")

location_counts = df["Location"].value_counts().head(10)
st.bar_chart(location_counts)

# -----------------------------
# TOP COMPANIES
# -----------------------------
st.subheader("🏢 Top Hiring Companies")

company_counts = df["Company"].value_counts().head(10)
st.bar_chart(company_counts)