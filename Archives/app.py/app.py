from flask import Flask, request, render_template
import sqlite3
import re
import requests
import os

app = Flask(__name__)

# -------------------------
# CLEAN SQL (remove ```sql fences)
# -------------------------
def clean_sql(sql):
    if not sql:
        return sql

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


# -------------------------
# AI FALLBACK FUNCTION
# -------------------------
def generate_sql_with_ai(text):
    api_key = os.getenv("PERPLEXITY_API_KEY")

    if not api_key:
        return None, "AI fallback unavailable: missing API key."

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": "Generate ONLY SQL. No explanation."},
                    {"role": "user", "content": text}
                ]
            },
            timeout=10
        )

        data = response.json()
        print("AI RAW RESPONSE:", data)

        # API error
        if "error" in data:
            return None, f"AI error: {data['error']}"

        # Standard OpenAI-style format
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]

            # message.content
            if "message" in choice and "content" in choice["message"]:
                sql = choice["message"]["content"].strip()
                return sql, None

            # text field
            if "text" in choice:
                sql = choice["text"].strip()
                return sql, None

        # Perplexity output_text format
        if "output_text" in data:
            sql = data["output_text"].strip()
            return sql, None

        return None, "AI returned an unexpected response."

    except Exception as e:
        return None, f"AI fallback error: {e}"


# -------------------------
# ROUTES
# -------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/query', methods=['POST'])
def query():
    text = request.form.get("text", "").lower()
    sql = None
    message = None
    results = []

    # -------------------------
    # RULE-BASED SQL
    # -------------------------
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

    # -------------------------
    # AI FALLBACK
    # -------------------------
    if sql is None:
        sql, ai_error = generate_sql_with_ai(text)

        if ai_error:
            message = ai_error
        elif sql:
            sql = clean_sql(sql)
            message = "AI-generated SQL (fallback used)."

    # -------------------------
    # EXECUTE SQL
    # -------------------------
    if sql:
        try:
            conn = sqlite3.connect("app.db")
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            if not rows:
                message = "No results found for your query."
            else:
                column_names = [desc[0] for desc in cursor.description]
                results = [dict(zip(column_names, row)) for row in rows]

        except Exception as e:
            message = f"SQL execution error: {e}"

        finally:
            conn.close()

    return render_template("index.html", sql=sql, results=results, message=message)


if __name__ == '__main__':
    app.run(debug=True)