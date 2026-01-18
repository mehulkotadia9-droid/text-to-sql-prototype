import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create Customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT
);
""")

# Create Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    price REAL,
    date TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customers(id)
);
""")

# Insert sample customers
cursor.executemany("INSERT INTO Customers (name, date) VALUES (?, ?)", [
    ("Alice", "2019-05-10"),
    ("Bob", "2021-07-22"),
    ("Charlie", "2023-01-15")
])

# Insert sample orders
cursor.executemany("INSERT INTO Orders (customer_id, price, date) VALUES (?, ?, ?)", [
    (1, 250, "2019-06-01"),
    (2, 600, "2021-08-01"),
    (3, 120, "2023-02-10")
])

conn.commit()
conn.close()

print("Database initialized with sample data.")