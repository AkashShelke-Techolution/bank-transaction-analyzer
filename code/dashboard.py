import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# PostgreSQL Database Connection Settings
DB_NAME = "bank_transaction_analyzer"
DB_USER = "postgres"
DB_PASSWORD = "31011950"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to fetch data using SQLAlchemy
@st.cache_data
def load_data():
    try:
        # Corrected SQLAlchemy engine connection string
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        query = """
        SELECT t.transaction_date, t.amount, COALESCE(c.category_name, 'Uncategorized') AS category_name, t.description
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.transaction_date DESC;
        """

        # Load data into pandas DataFrame
        df = pd.read_sql(query, engine)

        # Convert date to datetime format
        if not df.empty:
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])

        return df

    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

# Streamlit UI
st.title("💰 Bank Transaction Analyzer")
st.sidebar.header("Filters")

if df.empty:
    st.warning("⚠️ No transactions found in the database.")
else:
    # Filter by category
    categories = df["category_name"].unique().tolist()
    selected_category = st.sidebar.multiselect("Select Categories", categories, default=categories)

    # Filter by date range
    start_date = st.sidebar.date_input("Start Date", df["transaction_date"].min())
    end_date = st.sidebar.date_input("End Date", df["transaction_date"].max())

    # Apply filters
    filtered_df = df[
        (df["category_name"].isin(selected_category)) & 
        (df["transaction_date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
    ]

    # Display filtered transactions
    st.subheader("📋 Transaction Data")
    st.dataframe(filtered_df)

    # Total spending per category
    st.subheader("📊 Total Spending by Category")
    category_spending = filtered_df.groupby("category_name")["amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=category_spending.index, y=category_spending.values, ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Category")
    plt.ylabel("Total Spending (CHF)")
    plt.title("Total Spending by Category")
    st.pyplot(fig)

    # Monthly spending trend
    st.subheader("📈 Monthly Spending Trend")
    filtered_df["month"] = filtered_df["transaction_date"].dt.to_period("M")
    monthly_spending = filtered_df.groupby("month")["amount"].sum()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=monthly_spending.index.astype(str), y=monthly_spending.values, marker="o", ax=ax2)
    plt.xticks(rotation=45)
    plt.xlabel("Month")
    plt.ylabel("Total Spending (CHF)")
    plt.title("Monthly Spending Trend")
    st.pyplot(fig2)

    # Top 10 highest transactions
    st.subheader("🏆 Top 10 Highest Transactions")
    st.write(filtered_df.sort_values("amount", ascending=False).head(10))
