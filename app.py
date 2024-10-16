from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re  # Import regex module for response cleaning

# Configure Genai API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, question])
    return response.text

# Function to clean the generated SQL query
def clean_sql_query(raw_response):
    """
    Cleans the raw response from the AI model to extract the SQL query.
    Removes any Markdown syntax, language identifiers, and extra whitespace.
    """
    # Remove Markdown code block syntax if present
    # This handles both ```sql and ``` (without language)
    cleaned = re.sub(r"```(?:sql)?\s*", "", raw_response, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```", "", cleaned, flags=re.IGNORECASE)
    
    # Remove any leading/trailing whitespace
    cleaned = cleaned.strip()
    
    # Optionally, ensure the query ends with a semicolon
    if not cleaned.endswith(";"):
        cleaned += ";"
    
    return cleaned

# Function To retrieve query from the database
def read_sql_query(sql, db):
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return []

# Define Your Prompt as a string
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
SECTION, and MARKS.

For example:
Example 1 - How many entries of records are present?
The SQL command will be: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science class?
The SQL command will be: SELECT * FROM STUDENT WHERE CLASS = "Data Science";

**Important:** 
- **Do not** include any Markdown syntax (e.g., ```sql).
- **Do not** add any additional text or explanations.
- **Output only the raw SQL query,** ending with a semicolon.
"""

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Austin's Gemini App To Retrieve SQL Data")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL query..."):
            raw_sql = get_gemini_response(question, prompt)
            st.write(f"**Generated SQL Query:** {raw_sql}")
            sql_query = clean_sql_query(raw_sql)
            st.write(f"**Cleaned SQL Query:** {sql_query}")
        
        with st.spinner("Executing SQL query..."):
            response_rows = read_sql_query(sql_query, "student.db")
            if response_rows:
                st.subheader("The Response is:")
                for row in response_rows:
                    st.write(row)
            else:
                st.info("No data found or an error occurred.")
