# 📰 News Scrapper – Adverse Media Extraction Pipeline

This repository contains a **complete end‑to‑end adverse media news scraping and analysis pipeline** built in Python. The script automates:

- Fetching news from Google News RSS
- Resolving redirected URLs
- Extracting full article content
- Cleaning and deduplicating news
- Identifying crimes, law‑enforcement agencies, persons, locations
- Extracting monetary amounts (quantum)
- Generating keywords
- Producing a structured adverse media dataset

---

## 📁 Project Structure

```
News_Scrapper/
│
├── functions.py          # Core reusable functions
├── config_info.py        # Configuration for dates, crimes, regex, RSS topics
│
├── processing/
│   ├── feed_<month>.csv
│   ├── updated_feed_<month>.csv
│   └── updated_content_feed_<month>.csv
│
├── output/
│   └── final_adverse_media_<month>.csv
│
└── main_script.py        # Main execution script
```

---

## 🔧 Libraries Used

| Library | Purpose |
|------|--------|
| `pygooglenews` | Fetch Google News RSS feeds |
| `selenium` | Resolve redirected / blocked URLs |
| `newspaper3k`, `goose3` | Article content extraction |
| `BeautifulSoup` | HTML parsing |
| `spaCy` | NLP (NER: persons, locations) |
| `NLTK` | Tokenization |
| `sklearn (TF-IDF)` | Keyword extraction |
| `regex` | Pattern extraction (money, LEAs) |
| `pandas` | Data processing |
| `tqdm` | Progress tracking |

---

## ⚙️ Configuration (`config_info.py`)

All business logic is controlled via configuration.

### Key Config Variables

```python
month_for_scraping
start_date
end_date
crime_list
lea_regex
rename_lea
news_providers
rss_dict
```

### Purpose

- **Date range** → controls scraping window
- **crime_list** → keywords like fraud, money laundering, bribery etc.
- **lea_regex** → identifies agencies like ED, CBI, NIA
- **rename_lea** → standardizes LEA names
- **rss_dict** → list of Google News topics

This makes the pipeline reusable month‑by‑month without code changes.

---

## 🚀 Execution Flow (High Level)

```
Google News RSS
        ↓
Fetch Titles + Links
        ↓
Resolve Redirected URLs
        ↓
Extract Full Articles
        ↓
Cleaning & Deduplication
        ↓
Crime Detection
        ↓
NER (Person, Location)
        ↓
Keyword Extraction
        ↓
Final Adverse Media Output
```

---

# 🔍 Detailed Code Explanation

---

## 1️⃣ Imports and Initialization

```python
from News_Scrapper.functions import *
```

Imports all reusable utility functions such as:

- `get_titles()`
- `get_redirected_url_with_selenium()`
- `extract_article_content()`
- `remove_duplicates()`
- `person_tagger()`
- `locations()`
- `get_keywords_from_article()`

---

```python
gn = GoogleNews(lang='en', country='IN')
```

Initializes Google News for:
- English language
- Indian news sources

---

```python
nlp = spacy.load('en_core_web_lg')
```

Loads large spaCy NLP model used for:
- Person name detection
- Location detection

---

## 2️⃣ fetch_news_feed()

```python
def fetch_news_feed(date_range, from_, to_, rss_dict):
```

### Purpose
Fetches news **titles, publish dates, source and links** from Google News RSS.

### Workflow

1. Iterates over configured month
2. Converts dates to required format
3. Loops over RSS topics
4. Adds **random delay (3–6 minutes)** to avoid Google blocking
5. Calls `get_titles()`
6. Appends results into a dataframe

### Output

- Returns consolidated news feed dataframe

---

## 3️⃣ get_updated_url()

```python
def get_updated_url(df):
```

### Problem Solved
Google News links are redirected URLs.

### Solution
Uses **Selenium browser automation** to:

- Open Google redirect URL
- Capture final publisher URL

### Output

Adds a new column:

```
updated_link
```

This ensures accurate article scraping.

---

## 4️⃣ article_content()

```python
def article_content(df):
```

### Purpose
Fetches **full article body text**.

### Method
Uses combination of:

- Newspaper3k
- Goose3
- Requests + BeautifulSoup

Fallback logic ensures maximum extraction success.

### Output

Adds column:

```
article_content
```

---

## 5️⃣ Cleaning & Pre‑Processing

```python
df_news.dropna()
drop_duplicates()
minimum word length filters
```

Filters ensure:

- Meaningful articles only
- No short or spam news
- Removes duplicates
- Removes agency-only headlines

---

## 6️⃣ Quantum (Money) Extraction

```python
regexp_quantum = re.compile(...)
```

Extracts:

- ₹10 crore
- Rs 50 lakh
- $2 million

From both:
- Article body
- Title

Final output is standardized.

---

## 7️⃣ Law Enforcement Agency (LEA) Detection

```python
df_final['lea'] = re.finditer(lea_regex)
```

Detects agencies like:

- ED
- CBI
- NIA
- SFIO

Then normalizes names using:

```python
rename_leas()
```

---

## 8️⃣ Crime Identification

```python
df_final['crimes']
```

Matches article text against predefined crime list:

Examples:
- fraud
- money laundering
- corruption
- bribery
- terror funding

Returns list of crimes per article.

---

## 9️⃣ Named Entity Recognition (NER)

### 👤 Person Tagging

```python
df_final['person'] = df_final['article'].apply(person_tagger)
```

Extracts:
- Individual names
- Accused / suspects / officials

---

### 📍 Location Extraction

```python
df_final['locations'] = df_final['article'].apply(locations)
```

Extracts:
- Cities
- States
- Countries

Using spaCy NER.

---

## 🔑 Keyword Extraction

```python
def extract_article_keywords()
```

Uses **TF‑IDF Vectorizer** to generate top keywords from article text.

Output:

```
Keywords column
```

Useful for:
- Case summaries
- Dashboard analytics
- Search & clustering

---

## 📤 Final Output

```python
final_adverse_media_<month>.csv
```

### Columns Included

- title
- published_date
- source
- updated_link
- article
- crimes
- lea
- quantum
- person
- locations
- keywords

---

## ✅ Final Use Cases

This pipeline is suitable for:

- 🔍 Adverse media monitoring
- 🏦 AML / Compliance screening
- 🧾 Background verification (BGV)
- 🕵️ Financial Intelligence Units (FIU)
- 📊 Risk analytics dashboards

---

## ⚠️ Important Notes

- Selenium delays are intentional (anti‑blocking)
- Use VPN or rotating IP for large scale runs
- spaCy `en_core_web_lg` is required
- ChromeDriver must match Chrome version

---

## 📌 Summary

This codebase provides a **production‑grade adverse media extraction framework** combining:

- Web scraping
- NLP
- Regex intelligence
- Entity extraction
- Structured data output

It is modular, configurable, and scalable for enterprise compliance workflows.

---

✅ **End of README.md**

