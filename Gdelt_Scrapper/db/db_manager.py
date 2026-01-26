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

    """def search(self, filters: dict):
        query = "SELECT * FROM adverse_media WHERE 1=1"
        params = []

        for col, val in filters.items():
            if val:
                query += f" AND {col} LIKE ?"
                params.append(f"%{val}%")

        return pd.read_sql(query, self.conn, params=params)"""
    


    """def search(self, filters: dict):
        query = "SELECT * FROM adverse_media WHERE 1=1"
        params = []

        # --- Date range ---
        date_from = filters.get("date_from")
        date_to = filters.get("date_to")

        if date_from and date_to:
            query += " AND date BETWEEN ? AND ?"
            params.extend([date_from, date_to])
        elif date_from:
            query += " AND date >= ?"
            params.append(date_from)
        elif date_to:
            query += " AND date <= ?"
            params.append(date_to)

        # --- Text / LIKE based filters ---
        like_fields = {
            "title",
            "article"
        }

        for field in like_fields:
            values = filters.get(field)
            if values:
                values = values.split(',')
                for i in range(0, len(values)):
                    if i == 0:
                        query += f" AND {field} LIKE ?"
                        params.append(f"%{values[i]}%")

                    else:
                        query += f" OR {field} LIKE ?"
                        params.append(f"%{values[i]}%")

        # Selectbox based filters
        selectbox_fields = {"lea", "domain"}
        for field in selectbox_fields:
            values = filters.get(field)
            if values:
                #values = values.split(',')
                for i in range(0, len(values)):
                    if i == 0:
                        query += f" AND {field} LIKE ?"
                        params.append(f"%{values[i]}%")

                    else:
                        query += f" OR {field} LIKE ?"
                        params.append(f"%{values[i]}%")

        # --- ARN (exact match) ---
        arn = filters.get("ARN")
        if arn:
            query += " AND ARN = ?"
            params.append(arn)

        # --- Optional ordering ---
        query += " ORDER BY date DESC"
        print(query)

        return pd.read_sql(query, self.conn, params=params)
"""
    
    def search(self, filters: dict):
        query = "SELECT * FROM adverse_media WHERE 1=1"
        params = []

        # --- Date range ---
        date_from = filters.get("date_from")
        date_to = filters.get("date_to")

        if date_from and date_to:
            query += " AND date BETWEEN ? AND ?"
            params.extend([date_from, date_to])
        elif date_from:
            query += " AND date >= ?"
            params.append(date_from)
        elif date_to:
            query += " AND date <= ?"
            params.append(date_to)

        # --- LIKE-based fields ---
        like_fields = ["title", "article", "keywords"]

        for field in like_fields:
            values = filters.get(field)
            if values:
                values = [v.strip() for v in values.split(",")]
                query += " AND (" + " OR ".join([f"{field} LIKE ?"] * len(values)) + ")"
                params.extend([f"%{v}%" for v in values])

        # --- Multi-select selectbox fields ---
        selectbox_fields = ["lea", "domain"]

        for field in selectbox_fields:
            values = filters.get(field)
            if values:
                if isinstance(values, str):
                    values = values.split(",")
                values = [v.strip() for v in values if v.strip()]

                query += " AND (" + " OR ".join([f"{field} LIKE ?"] * len(values)) + ")"
                params.extend([f"%{v}%" for v in values])

        # --- ARN ---
        arn = filters.get("ARN")
        if arn:
            query += " AND ARN = ?"
            params.append(arn)

        query += " ORDER BY date DESC"
        print(query)

        return pd.read_sql(query, self.conn, params=params)


    def get_max_date(self):
        query = "SELECT MAX(date) AS max_date, min(date) as min_date FROM adverse_media limit1"
        return pd.read_sql(query, self.conn)

    def get_distinct_values(self, column):
        query = f"SELECT DISTINCT {column} FROM adverse_media WHERE {column} IS NOT NULL"
        rows = self.fetch_all(query)
        return sorted([r[column] for r in rows if r[column]])

