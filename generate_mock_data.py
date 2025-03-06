import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for random data
fake = Faker()

# PostgreSQL Database Connection Settings 
DB_NAME = "bank_transaction_analyzer"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"  # Default PostgreSQL port

# Establishes Database Connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Connected to the database successfully!")

except Exception as e:
    print("Error connecting to the database:", e)
    exit()

# Retrieves category IDs from the database
cursor.execute("SELECT category_id FROM categories;")
categories = [row[0] for row in cursor.fetchall()]

if not categories:
    print("No categories found. Please insert categories first!")
    exit()

# Generates mock transactions
num_transactions = 500
transactions = []

for _ in range(num_transactions):
    transaction_date = fake.date_between(start_date="-1y", end_date="today")  # Last year to today
    amount = round(random.uniform(5, 500), 2)  # Random amount between 5 and 500
    category_id = random.choice(categories)  # Random category
    description = fake.sentence(nb_words=6)  # Random short description

    transactions.append((transaction_date, amount, category_id, description))

# Inserts generated transactions into the database
insert_query = """
    INSERT INTO transactions (transaction_date, amount, category_id, description)
    VALUES (%s, %s, %s, %s);
"""

try:
    cursor.executemany(insert_query, transactions)
    conn.commit()
    print(f"{num_transactions} mock transactions inserted successfully!")

except Exception as e:
    conn.rollback()
    print("Error inserting transactions:", e)

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
