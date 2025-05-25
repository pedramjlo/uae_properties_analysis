import streamlit as st

import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loading_db.loadtoDB import Database


db = Database()




st.set_page_config(page_title="SQL File Dashboard", layout="wide")
st.title("📊 Dashboard from SQL File")

# Choose category (example filter)
engine = db.create_engine()
categories = pd.read_sql("SELECT DISTINCT City FROM uae_properties", engine)["City"].tolist()
selected_category = st.selectbox("Select City", categories)


# Load and format the SQL file
with open("analysis/main.sql") as f:
    sql = f.read()

# Execute query with parameter
df = pd.read_sql(sql, engine, params={"City": selected_category})

# Plot
st.subheader(f"All cities: {selected_category}")
st.line_chart(df.set_index("month")["total_revenue"])


