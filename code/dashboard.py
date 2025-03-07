import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Load database credentials from Streamlit secrets
DB_USERNAME = st.secrets["neondb_owner"]
DB_PASSWORD = st.secrets["npg_wBgu6zemHo5O"]
DB_HOST = st.secrets["ep-old-tooth-a9ie9a72-pooler.gwc.azure.neon.tech"]
DB_PORT = st.secrets["5432"]
DB_NAME = st.secrets["neondb"]
DB_SSLMODE = st.secrets["require"]

# Construct the database URL dynamically
DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

@st.cache_data
def load_data():
    try:
        engine = create_engine(DB_URL)  # Connect to Neon.tech
        query = """
        SELECT t.transaction_date, t.amount, COALESCE(c.category_name, 'Uncategorized') AS category_name, t.description
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.transaction_date DESC;
        """
        df = pd.read_sql(query, engine)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        return df
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return pd.DataFrame()
