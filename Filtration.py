import streamlit as st
import pandas as pd
import mysql.connector
import re

def parse_voating_string(value):
    try:
        if pd.isna(value):
            return 0
        value = str(value).strip().replace(",", "").replace("(", "").replace(")", "").upper()
        match = re.match(r'^([\d\.]+)([KMB]?)$', value)
        if not match:
            return 0
        num, suffix = match.groups()
        num = float(num)
        if suffix == 'K':
            return int(num * 1_000)
        elif suffix == 'M':
            return int(num * 1_000_000)
        elif suffix == 'B':
            return int(num * 1_000_000_000)
        else:
            return int(num)
    except:
        return 0
def parse_duration(value):
    try:
        if pd.isna(value):
            return 0
        value = str(value).lower().replace("hrs", "").replace("hr", "").replace("hours", "").strip()
        return float(re.findall(r"[\d.]+", value)[0])
    except:
        return 0
def load_movies_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="Shankar",
        password="NewPassword123!",
        database="movies_2024"
    )
    query = "SELECT Titles, Genre, Ratings, Voatings, Duration FROM movies_2024"
    df = pd.read_sql(query, conn)
    conn.close()   
    return df

df= load_movies_data()
df.columns = [col.strip().capitalize() for col in df.columns]
df["Voatings"] = df["Voatings"].apply(parse_voating_string)
df["Duration"] = df["Duration"].apply(parse_duration)
if df.empty or df["Voatings"].max() <= 0:
    st.error("No valid voating data found. Please check your database or parsing logic.")
    st.dataframe(df)
    st.stop()
st.sidebar.header(" Filter Movies")

unique_genres = sorted(df["Genre"].dropna().unique())
selected_genre = st.sidebar.selectbox(" Select Genre:", ["All"] + list(unique_genres))

# Ratings Filter
min_rating = float(df["Ratings"].min())
max_rating = float(df["Ratings"].max())
selected_rating = st.sidebar.slider(" Minimum IMDb Rating:", min_value=min_rating, max_value=max_rating, value=min_rating)

# Voatings Filter
min_voatings = int(df["Voatings"].min())
max_voatings = int(df["Voatings"].max())
selected_voatings = st.sidebar.slider(" Minimum Voatings:", min_value=min_voatings, max_value=max_voatings, value=min_voatings)

# Duration Filter
duration_filter = st.sidebar.radio(" Movie Duration:", ["< 2 hrs", "2–3 hrs", "> 3 hrs"])
filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

filtered_df = filtered_df[filtered_df["Ratings"] >= selected_rating]
filtered_df = filtered_df[filtered_df["Voatings"] >= selected_voatings]

if duration_filter == "< 2 hrs":
    filtered_df = filtered_df[filtered_df["Duration"] < 2]
elif duration_filter == "2–3 hrs":
    filtered_df = filtered_df[(filtered_df["Duration"] >= 2) & (filtered_df["Duration"] <= 3)]
else:
    filtered_df = filtered_df[filtered_df["Duration"] > 3]


# Display Results
st.success(f"🎉 Found {len(filtered_df)} matching movies!")
st.dataframe(filtered_df)
