import pandas as pd
import numpy as np
import random
import time
import re
from tqdm import tqdm
from gdeltdoc import GdeltDoc, Filters

from functions import *
from config_info import *
from logger import get_logger

logger = get_logger("AdverseMediaPipeline")

# ======================================================
# Utility
# ======================================================

def remove_illegal(text: str) -> str:
    if not isinstance(text, str):
        return text
    return "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)


# ======================================================
# Fetch Articles
# ======================================================

def fetch_article_links(gd, start_date, end_date, keyword):
    filters = Filters(
        start_date=start_date,
        end_date=end_date,
        keyword=keyword,
        country="India",
        language="English",
        tone="<-1"
    )
    return gd.article_search(filters)


def fetch_all_articles(start_date, end_date, keywords):
    gd = GdeltDoc()
    dfs = []

    logger.info(f"Starting article fetch for {len(keywords)} keywords")

    for keyword in tqdm(keywords):
        delay = random.randint(30, 90) / 60
        logger.info(f"Keyword: {keyword} | sleeping {round(delay,2)} minutes")
        time.sleep(delay)

        try:
            df = fetch_article_links(gd, start_date, end_date, keyword)
            logger.info(f"{keyword} → fetched {len(df)} records")
            dfs.append(df)

        except Exception as e:
            logger.exception(f"Failed fetching keyword: {keyword}")

    logger.info("Article fetching completed")
    return pd.concat(dfs, ignore_index=True)


###################################################################
# Article Content Extraction
###################################################################
def fetch_article_content(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Fetching article content for {len(df)} URLs")

    contents = []

    for url in tqdm(df["url"]):
        try:
            contents.append(extract_article_content(url))
        except Exception:
            logger.warning(f"Failed article extraction: {url}")
            contents.append(None)

    df["article_content"] = contents
    df = df[df["article_content"].notna()]

    logger.info(f"Successfully extracted {len(df)} articles")
    return df

###################################################################
# Domain Filtering 
###################################################################
def filter_domains(df, domains):
    logger.info("Filtering allowed domains")

    domain_pattern = "|".join(domains)
    df = df[df["domain"].str.lower().str.contains(domain_pattern, na=False)]

    logger.info(f"Remaining after domain filter: {len(df)}")
    return df

###################################################################
# Keyword Extraction
###################################################################
def extract_article_keywords(df):
    logger.info("Extracting article keywords")

    df["Keywords"] = df["article"].apply(
        lambda x: get_keywords_from_article(x, 5) if isinstance(x, str) else None
    )
    return df




########################################################
#Function to prepare data for uploading in DB
########################################################
from datetime import date
def prepare_for_db(df):
    # adding unique ARN
    df = df.reset_index()
    today = date.today().strftime('%Y%m%d')
    df['ARN'] = 'ARN'+today+df['index'].astype('str')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    columns = ['ARN', 'date', 'title', 'article', 'domain', 'url', 'lea', 'crimes',
        'person', 'locations', 'quantum', 'Keywords' ]
    df = df[columns]
    return df

###################################################################
# store to sqlite db
###################################################################
from db.db_manager import AdverseMediaDB

def store_to_sqlite(df_final):
    db = AdverseMediaDB()
    db.create_table()
    db.insert_dataframe(df_final)



###################################################################
# Main Pipeline Runner
###################################################################
def run_pipeline():

    logger.info("========== PIPELINE STARTED ==========")

    # Step 1: Fetch URLs
    df_links = fetch_all_articles(from_, to_, keywords)
    df_links.to_csv(f"./processing/raw_feed_{month_name}.csv", index=False)

    df_links.drop_duplicates(subset="url", inplace=True)

    # Step 2: Domain filter
    df_links = filter_domains(df_links, domains)
    df_links.to_csv(f"./processing/filtered_feed_{month_name}.csv", index=False)

    # Step 3: Article content
    df_articles = fetch_article_content(df_links)
    df_articles.to_csv(f"./processing/article_content_{month_name}.csv", index=False)

    # Step 4: Cleaning
    df_articles["title"] = df_articles["title"].astype(str).apply(remove_illegal)
    df_articles["article_content"] = df_articles["article_content"].astype(str).apply(remove_illegal)

    df_articles.rename(
        columns={"article_content": "article", "seendate": "date"},
        inplace=True
    )

    df_articles["date"] = df_articles["date"].astype(str).str[:8]

    df_articles = remove_duplicates(df_articles)

    # Step 5: Enrichment
    regexp_quantum = re.compile(
        r'((?: Rs|₹|\$)(?:.| )?[0-9]+[0-9.,]*[a-z]?(?: |-)(?:lacs|crores|million|lakh|billion|crore|cr)? ?(?:rupees|rupee|dollars|dollar)?)',
        re.IGNORECASE
    )

    df_articles["quantum"] = (
        df_articles["article"].apply(lambda x: regexp_quantum.findall(str(x))) +
        df_articles["title"].apply(lambda x: regexp_quantum.findall(str(x)))
    )

    df_articles["quantum"] = df_articles["quantum"].apply(
        lambda x: list(set(i.replace("₹", "Rs ").replace("-", "").strip() for i in x))
    )

    df_articles["lea"] = df_articles["article"].apply(
        lambda x: rename_leas(
            list(set(i.group().strip() for i in re.finditer(lea_regex, str(x).upper())))
        )
    )

    df_articles["crimes"] = (
        df_articles["article"].apply(lambda x: [c for c in crime_list if c in x.lower()]) +
        df_articles["title"].apply(lambda x: [c for c in crime_list if c in x.lower()])
    )

    df_articles["crimes"] = df_articles["crimes"].apply(lambda x: list(set(x)))

    df_articles["person"] = df_articles["article"].apply(person_tagger)
    df_articles["locations"] = df_articles["article"].apply(locations)

    df_articles = extract_article_keywords(df_articles)

    # Step 6: Output
    output_path = f"./output/final_adverse_media_{month_name}.csv"
    df_articles.to_csv(output_path, index=False)

    # prepare to store in DB
    df_articles = prepare_for_db(df_articles)
    
    # Step 7: storing to db
    logger.info(f"storing fetched article for {month_name} to database")
    store_to_sqlite(df_articles)


    logger.info(f"Pipeline completed successfully → {output_path}")
    logger.info("========== PIPELINE FINISHED ==========")


if __name__ == "__main__":
    run_pipeline()







