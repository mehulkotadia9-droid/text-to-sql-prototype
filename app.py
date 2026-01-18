from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    text = request.form.get("text", "").lower()

    if "list all customers" in text:
        sql = "SELECT * FROM Customers;"

    elif "orders greater than" in text:
        match = re.search(r'greater than (\d+)', text)
        amount = match.group(1) if match else "500"
        sql = f"SELECT * FROM Orders WHERE price > {amount};"

    elif "customers after" in text:
        match = re.search(r'after (\d{4})', text)
        year = match.group(1) if match else "2020"
        sql = f"SELECT * FROM Customers WHERE date > '{year}-01-01';"

    elif "orders for" in text:
        match = re.search(r'orders for ([a-zA-Z]+)', text)
        name = match.group(1).capitalize() if match else ""
        sql = f"""
            SELECT Orders.*
            FROM Orders
            JOIN Customers ON Orders.customer_id = Customers.id
            WHERE Customers.name = '{name}';
        """

    elif "total sales by customer" in text:
        sql = """
            SELECT Customers.name, SUM(Orders.price) AS total_sales
            FROM Orders
            JOIN Customers ON Orders.customer_id = Customers.id
            GROUP BY Customers.name;
        """

    elif "latest" in text and "orders" in text:
        match = re.search(r'latest (\d+)', text)
        limit = match.group(1) if match else "5"
        sql = f"SELECT * FROM Orders ORDER BY date DESC LIMIT {limit};"

    elif "customers before" in text:
        match = re.search(r'before (\d{4})', text)
        year = match.group(1) if match else "2022"
        sql = f"SELECT * FROM Customers WHERE date < '{year}-01-01';"

    elif "orders between" in text:
        match = re.search(r'between (\d+) and (\d+)', text)
        low, high = match.groups() if match else ("100", "500")
        sql = f"SELECT * FROM Orders WHERE price BETWEEN {low} AND {high};"

    else:
        sql = None

    results = []
    if sql:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]
        conn.close()

    return render_template("index.html", sql=sql, results=results)

if __name__ == '__main__':
    app.run(debug=True)