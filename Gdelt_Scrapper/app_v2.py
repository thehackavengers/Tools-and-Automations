import streamlit as st
import pandas as pd
from db.db_manager import AdverseMediaDB
import config_info as info
from pipeline import *
from datetime import date, datetime


#lea_list
lea_list = info.rename_lea
news_domains = info.domains


st.set_page_config(
    page_title="Adverse Media Analyser",
    layout="wide"
)

st.title("🕵️ Adverse Media Analyser")
st.caption("Search, filter and analyse adverse media articles")

db = AdverseMediaDB()

# -------------------------------
# Show max available date
# -------------------------------
max_date = db.get_max_date()  # expects DATE or YYYY-MM-DD
#if max_date:
st.info(f"📊 This database holds data from **{max_date.iloc[0][1]}** till **{max_date.iloc[0][0]}**")

# -------------------------------
# Update Data Button
# -------------------------------
if st.button("Update Data"):
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    month_name= f'manual_update_{now}'
    from_ = max_date.iloc[0][0]
    to_ = date.today().strftime("%Y-%m-%d")
    st.info(f"Updating data from {from_} till {to_}")
    for i in range(101):
        st.progress(i)
        run_pipeline()
    st.success(f"Data updated successfully!!")


# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Search Filters")

# ---- Date Range (Calendar) ----
st.sidebar.subheader("📅 Date Range")

from_date = st.sidebar.date_input(
    "Select date from_:",
    value= None,
    min_value=date(2025, 4, 1),
    max_value=date.today()
)

to_date = st.sidebar.date_input(
    "Select date till_:",
    value= None,
    min_value=from_date,
    max_value=date.today()
)

title = st.sidebar.text_input("Title contains")
keywords = st.sidebar.text_input("Keywords separated by comma")



# ---- Dynamic LEA list ----
#lea_options = db.get_distinct_values("lea")
lea_options = set([value for value in lea_list.values()])
selected_leas = st.sidebar.multiselect(
    "Law Enforcement Agencies",
    options=lea_options
)

# ---- Dynamic Domain list ----
#domain_options = db.get_distinct_values("domain")
domain_options = news_domains
selected_domains = st.sidebar.multiselect(
    "News Domains",
    options=domain_options
)

filters = {
    "title": title,
    "article": keywords,
    "lea": selected_leas,
    "domain": selected_domains,
    "date_from": from_date,
    "date_to": to_date
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

arn = st.text_input("Enter ARN (e.g. ARN2025120101)")

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
