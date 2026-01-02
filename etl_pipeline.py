import pandas as pd
import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="fleximart"
)
cursor = conn.cursor()

# ------------------ CUSTOMERS ------------------
customers = pd.read_csv("customers_raw.csv")

customers.drop_duplicates(inplace=True)
customers.dropna(subset=['email'], inplace=True)

customers['phone'] = customers['phone'].astype(str).str.replace(r'\D', '', regex=True)
customers['phone'] = '+91' + customers['phone'].str[-10:]

customers['registration_date'] = pd.to_datetime(customers['registration_date']).dt.date

for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, tuple(row[1:]))

conn.commit()

# ------------------ PRODUCTS ------------------
products = pd.read_csv("products_raw.csv")

products.dropna(subset=['price'], inplace=True)
products['category'] = products['category'].str.strip().str.title()
products['stock_quantity'].fillna(0, inplace=True)

for _, row in products.iterrows():
    cursor.execute("""
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (%s,%s,%s,%s)
    """, tuple(row[1:]))

conn.commit()

# ------------------ SALES ------------------
sales = pd.read_csv("sales_raw.csv")
sales.drop_duplicates(inplace=True)
sales.dropna(subset=['customer_id', 'product_id'], inplace=True)
sales['order_date'] = pd.to_datetime(sales['order_date']).dt.date

for _, row in sales.iterrows():
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (%s,%s,%s)
    """, (row['customer_id'], row['order_date'], row['total_amount']))

conn.commit()

print("ETL Pipeline executed successfully.")

