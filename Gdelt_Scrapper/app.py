import streamlit as st
import pandas as pd
from db.db_manager import AdverseMediaDB

st.set_page_config(
    page_title="Adverse Media Analyser",
    layout="wide"
)

st.title("🕵️ Adverse Media Analyser")
st.caption("Search, filter and analyse adverse media articles")

db = AdverseMediaDB()

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("🔍 Search Filters")

title = st.sidebar.text_input("Title contains")
person = st.sidebar.text_input("Person name")
crime = st.sidebar.text_input("Crime keyword")
lea = st.sidebar.text_input("Law Enforcement Agency")
location = st.sidebar.text_input("Location")
domain = st.sidebar.text_input("Domain")
keyword = st.sidebar.text_input("Keyword")
date = st.sidebar.text_input("Date (YYYYMMDD)")

filters = {
    "title": title,
    "person": person,
    "crimes": crime,
    "lea": lea,
    "locations": location,
    "domain": domain,
    "keywords": keyword,
    "date": date
}

# -------------------------------
# Search Button
# -------------------------------

if st.sidebar.button("🔎 Search"):

    df = db.search(filters)

    st.subheader(f"Results Found: {len(df)}")

    if df.empty:
        st.warning("No matching articles found.")
    else:
        st.dataframe(
            df[
                [
                    "ARN", "date", "title", "domain", "person",
                    "crimes", "lea", "locations", "quantum"
                ]
            ],
            use_container_width=True
        )

        st.download_button(
            "⬇ Download Results",
            df.to_csv(index=False),
            file_name="adverse_media_results.csv"
        )

# -------------------------------
# Article Viewer
# -------------------------------

st.divider()
st.subheader("📄 Article Viewer")

arn = st.text_input("Enter ARN in ARN2025120101 format")

if st.button("View Article"):
    article_df = db.search({"ARN": str(arn)})

    if not article_df.empty:
        row = article_df.iloc[0]

        st.markdown(f"### {row['title']}")
        st.markdown(f"**Date:** {row['date']}  ")
        st.markdown(f"**Domain:** {row['domain']}  ")
        st.markdown(f"**URL:** {row['url']}")

        st.divider()
        st.write(row["article"])
    else:
        st.error("Article not found.")
