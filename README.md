 Text‑to‑SQL Prototype (Rule‑Based + AI Hybrid)
A hybrid Text‑to‑SQL engine built with Flask, combining:
- Fast rule‑based SQL generation
- Flexible AI‑powered SQL generation using the Perplexity API
- Safe SQL execution with validation
- A simple web UI for natural‑language queries
This project demonstrates how natural language can be converted into SQL queries and executed against a SQLite database.

🚀 Features

🔹 Rule‑Based SQL Generation
Handles common patterns such as:
- list all customers
- orders greater than X
- orders between X and Y
- latest N orders
- total sales by customer
- last order date

🔹 AI Fallback (Perplexity API)
When no rule matches, the app:
- Sends the query to Perplexity
- Receives SQL
- Cleans Markdown formatting
- Validates SQL for safety
- Executes it if safe

🔹 SQL Safety Layer
Prevents dangerous queries:
- Blocks DROP, DELETE, UPDATE, INSERT, ALTER
- Ensures SQL begins with SELECT or WITH
- Rejects non‑SQL responses

🔹 Web UI
A simple HTML interface that:
- Accepts natural language
- Displays generated SQL
- Shows query results in a table

📂 Project Structure
rule_based_prototype/
│
├── app.py
├── app.db
├── init_db.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── venv/



🛠️ Installation & Setup
1. Clone the repository
git clone https://github.com/mehulkotadia9-droid/text-to-sql-prototype.git
cd text-to-sql-prototype


2. Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash


3. Install dependencies
pip install -r requirements.txt


4. Initialize the database (optional)
python init_db.py


5. Set your Perplexity API key
export PPLX_API_KEY="your_api_key_here"



▶️ Running the Application
Start the Flask server:
python app.py


Open your browser:
http://127.0.0.1:5000/



🧪 Example Queries
Try rule‑based queries:
- list all customers
- orders greater than 200
- orders between 100 and 300
- latest 5 orders
- last order date
Try AI‑powered queries:
- customers who spent more than 200 last year
- show customers with high spending
- orders from loyal customers

🩺 Troubleshooting
Blank page
Ensure index.html is inside templates/.
AI not triggered
Check terminal logs for:
NO RULE MATCHED — AI SHOULD RUN


AI returns explanations instead of SQL
Strengthen the system prompt.
SQL appears but no results
Your database may not contain matching data (e.g., date ranges).
500 error
AI returned non‑SQL text — validation will block it.

🌍 Deployment
This app can be deployed to:
- Render (recommended)
- PythonAnywhere
- Railway
- AWS / Azure / GCP
- Docker containers
Environment variables must be set on the hosting platform.

📄 License
MIT License (optional — add if you want)

🙌 Acknowledgements
- Perplexity API for AI SQL generation
- Flask for backend routing
- SQLite for lightweight storage
