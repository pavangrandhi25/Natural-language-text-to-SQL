referal link: https://www.youtube.com/watch?v=wFdFLWc-W4k

# Network Inventory — NL → SQLite (Streamlit + Gemini)

Overview
- Purpose: Convert plain-English questions into SQLite SELECT queries for a small network-device inventory and display results in a Streamlit UI.
- Key files: `app.py`, `schema.py`, `sql.py`, `requirements.txt`, `.env`

Requirements
- Python 3.8+
- Install dependencies:
```bash
pip install -r requirements.txt
```
- Set your Google API key in `.env`:
```
GOOGLE_API_KEY=your_api_key_here
```

Initialize the database
- Create tables and seed example data:
```bash
python schema.py
```
- This creates `network_devices_inventory.db` with tables: `device`, `interface`, `connectivity`, `mac_table`. `schema.py` uses `INSERT OR IGNORE` so repeated runs are safe.

Run the Streamlit app
- Start the app:
```bash
streamlit run app.py
```
- Flow: enter a natural-language question → model converts it to a SQLite SELECT query → the app executes the query and displays results.
