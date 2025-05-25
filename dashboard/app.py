import streamlit as st
import pandas as pd
import sys
import os

# Add project root to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loading_db.loadtoDB import Database

# Instantiate your Database class once
db = Database()

st.set_page_config(page_title="SQL File Dashboard", layout="wide")
st.title("📊 Dashboard from SQL File")

# Create DB engine
engine = db.create_engine()

# Fetch categories (cities)
try:
    categories = pd.read_sql("SELECT DISTINCT city FROM uae_properties", engine)["city"].tolist()
except Exception as e:
    st.error(f"Error fetching cities: {e}")
    st.stop()

selected_category = st.selectbox("Select city", categories)

# Read SQL query file
with open("analysis/national_stats/main.sql") as f:
    sql = f.read()

# Run parameterized query
try:
    df = pd.read_sql(sql, engine, params={"city": selected_category})
except Exception as e:
    st.error(f"Error executing query: {e}")
    st.stop()

