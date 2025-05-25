import streamlit as st
import pandas as pd
import sys, os

# Setup import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from loading_db.loadtoDB import Database


from analysis.sql.load_named_queries import load_named_queries 




# DB connection
db = Database()
engine = db.create_engine()

# UI: Analysis scope
cities = pd.read_sql("SELECT DISTINCT city FROM uae_properties", engine)["city"].tolist()
options = ["UAE National Analysis"] + sorted(cities)
selected = st.selectbox("Choose analysis scope", options)

# Load appropriate SQL file
if selected == "National":
    queries = load_named_queries("analysis/sql/national_analysis/national.sql")
    sql = queries["revenue_overview"]
    df = pd.read_sql(sql, engine)
else:
    queries = load_named_queries("analysis/sql/cities_analysis/city.sql")
    sql = queries["revenue_by_city"]
    df = pd.read_sql(sql, engine, params={"city": selected})

# Display
st.subheader(f"📊 {'UAE' if selected == 'National' else selected} Revenue Over Time")
st.line_chart(df.set_index("month")["total_revenue"])
