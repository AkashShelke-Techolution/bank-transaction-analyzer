matplotlib
seaborn

import streamlit as st
import pandas as pd


CSV_URL = "https://raw.githubusercontent.com/oksanalim/bank-transaction-analyzer/refs/heads/main/data/transactions.csv"

@st.cache_data
def load_data():
    """Loads transaction data from GitHub CSV."""
    try:
        df = pd.read_csv(CSV_URL)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        return df
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Load data
df = load_data()

# Streamlit UI
st.title("💰 Bank Transaction Analyzer")

# Show dataframe
if not df.empty:
    st.dataframe(df)
else:
    st.warning("⚠️ No transactions found. Please check the data source.")
