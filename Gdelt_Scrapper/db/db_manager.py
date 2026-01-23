import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("database/adverse_media.db")

class AdverseMediaDB:

    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS adverse_media (
                ARN TEXT PRIMARY KEY,
                date DATE,
                title TEXT,
                article TEXT,
                domain TEXT,
                url TEXT UNIQUE,
                lea TEXT,
                crimes TEXT,
                person TEXT,
                locations TEXT,
                quantum TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_dataframe(self, df: pd.DataFrame):
        df = df.copy()

        # convert lists → string
        list_cols = ["lea", "crimes", "person", "locations", "quantum", "Keywords"]
        for col in list_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)

        df.rename(columns={"Keywords": "keywords"}, inplace=True)

        df.to_sql(
            "adverse_media",
            self.conn,
            if_exists="append",
            index=False
        )

    def search(self, filters: dict):
        query = "SELECT * FROM adverse_media WHERE 1=1"
        params = []

        for col, val in filters.items():
            if val:
                query += f" AND {col} LIKE ?"
                params.append(f"%{val}%")

        return pd.read_sql(query, self.conn, params=params)
