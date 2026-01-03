import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genAI

load_dotenv()
genAI.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#function to convert natural language text to sql query
def get_gemini_response(question,prompt):
    model = genAI.GenerativeModel(model_name='gemini-3-flash-preview')
    response = model.generate_content([prompt,question])
    return response.text

#function to retrieve data from the database with query
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.commit()
    conn.close()

    for row in rows:
        print(row)

    return rows

#define prompt
prompt = """You are a SQL query generator for a network device inventory database. 
Convert natural language questions into valid SQLite queries.

Database schema:
- device (device_id, name, type, ip_addr, mac_addr, vendor, location)
- interface (interface_id, device_id, interface_name, interface_type)
- connectivity (link_id, from_interface_id, to_interface_id, link_type)
- mac_table (mac_id, switch_device_id, mac_address, interface_id)

Example 1:
Question: "Show all routers in the network"
SQL Query: SELECT * FROM device WHERE type = 'ROUTER';

Example 2:
Question: "List all devices located in the lab"
SQL Query: SELECT name, type, location FROM device WHERE location = 'Lab';

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQLite syntax
- Join tables when necessary
- Use WHERE clauses for filtering
- Return SELECT statements only (no INSERT, UPDATE, DELETE)

Now convert this question to a SQL query:
"""

#streamlit app
st.set_page_config(page_title='Network Devices Inverntory')
st.header('Retrieve the data from Lab Inventory')

question = st.text_input("Question: ",key="input")
submit = st.button("Submit")

if submit:
    response = get_gemini_response(question,prompt)
    print("response o/p : ",response)

    data = read_sql_query(response,"network_devices_inventory.db")
    st.subheader("Answer: ")
    for row in data:
        print(row)
        st.header(row)