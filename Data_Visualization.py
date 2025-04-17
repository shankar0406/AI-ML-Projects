import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def load_movies_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="Shankar",
        password="NewPassword123!",
        database="movies_2024"
    )
    query = "SELECT Titles, Genre, Ratings, Voatings, Duration FROM movies_2024;"
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    conn.close()

    df['Voatings'] = df['Voatings'].astype(str).str.replace('K', '000').str.replace(',', '').str.extract(r'(\d+)')
    df['Voatings'] = pd.to_numeric(df['Voatings'], errors='coerce').fillna(0)
    df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce').fillna(0)

    df = df.sort_values(by=['Voatings'], ascending=False).drop_duplicates(subset=['Titles'], keep='first')


    df['Score'] = (df['Ratings'] * 0.5) + (df['Voatings'] * 0.5)

    return df


df = load_movies_data()

# 1: Identify top 10 movies using Ratings & Voatings
top_movies = df.sort_values(by=['Score'], ascending=False).head(10)

st.title("1 : Top 10 Movies Based on Both Ratings and Voatings")
st.write(top_movies)

fig, ax = plt.subplots(figsize=(12, 6))
top_movies.plot(x='Titles', y=['Ratings', 'Voatings', 'Score'], kind='bar', ax=ax, color=['skyblue', 'orange', 'red'])
ax.set_title("Top 10 Movies Ranked by Ratings & Voatings")
ax.set_xlabel("Movie Titles")
ax.set_ylabel("Scores")
plt.xticks(rotation=45)
st.pyplot(fig)

# 2: Movies Distribution by Genre

genre_counts = df['Genre'].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
genre_counts.plot(kind='bar', color='purple', ax=ax)
ax.set_title("Number of Movies per Genre (EDA)")
ax.set_xlabel("Genre")
ax.set_ylabel("Movie Count")
plt.xticks(rotation=45)
st.subheader("2 :  Movies Distribution by Genre")
st.pyplot(fig)

# 3: average movie duration per genre in a horizontal bar chart.

df['Duration'] = df['Duration'].astype(str).str.extract(r'(\d+)')
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
df['Duration'].fillna(df['Duration'].mean(), inplace=True)

df['Genre'] = df['Genre'].str.strip().str.lower()

print(df['Genre'].value_counts())
avg_duration_per_genre = df.groupby('Genre', as_index=False)['Duration'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(avg_duration_per_genre['Genre'], avg_duration_per_genre['Duration'], color='green')
ax.set_title("Average Movie Duration per Genre (EDA)")
ax.set_xlabel("Average Duration (minutes)")
ax.set_ylabel("Genre")
plt.xticks(rotation=0)
st.subheader("3 :  Average Movie Duration per Genre")
st.pyplot(fig)

#4: Visualize average voting counts across different genres.

df['Voatings'] = df['Voatings'].astype(str).str.replace('K', '000').str.extract(r'(\d+)') 
df['Voatings'] = pd.to_numeric(df['Voatings'], errors='coerce').fillna(0)

df['Genre'] = df['Genre'].str.strip().str.lower()
avg_voting_per_genre = df.groupby('Genre')['Voatings'].mean().sort_values()

fig, ax = plt.subplots(figsize=(12, 6))
avg_voting_per_genre.plot(kind='bar', color='blue', ax=ax)
ax.set_title("Average Voting Counts per Genre (EDA)")
ax.set_xlabel("Genre")
ax.set_ylabel("Average Voting Count")
plt.xticks(rotation=45)
st.subheader("4 :  Average Voting Counts per Genre")
st.pyplot(fig)

#5: Display a histogram or boxplot of movie ratings.

df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
df.dropna(subset=['Ratings'], inplace=True)

# 5-a Create Histogram
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(df['Ratings'], bins=20, kde=True, color='blue', ax=ax)
ax.set_title("Histogram of Movie Ratings")
ax.set_xlabel("Ratings")
ax.set_ylabel("Frequency")
st.subheader("5-a) :Movie Ratings Distribution - Histogram")
st.pyplot(fig)

#5-b Create Boxplot
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(y=df['Ratings'], color='red', ax=ax)
ax.set_title("Boxplot of Movie Ratings")
ax.set_ylabel("Ratings")
st.subheader("5-b) : Movie Ratings Spread - Boxplot")
st.pyplot(fig)

#6: top-rated movie for each genre in a table.

df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
top_movies_by_genre = df.loc[df.groupby('Genre')['Ratings'].idxmax(), ['Genre', 'Titles', 'Ratings']]
st.subheader("6 : Top-Rated Movie for Each Genre")
st.write(top_movies_by_genre)

# 7: genres with the highest total voting counts in a pie chart.
df['Voatings'] = df['Voatings'].astype(str).str.replace('K', '000').str.extract(r'(\d+)')
df['Voatings'] = pd.to_numeric(df['Voatings'], errors='coerce').fillna(0)
df['Genre'] = df['Genre'].str.strip().str.lower()
genre_voting_totals = df.groupby('Genre')['Voatings'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(genre_voting_totals, labels=genre_voting_totals.index, autopct='%1.1f%%', colors=['blue', 'orange', 'green', 'purple', 'red'])
ax.set_title("Genres with Highest Total Voting Counts (EDA)")
st.subheader("7 : Genres with Highest Total Voting Counts")
st.pyplot(fig)

# 8:Use a table to show the shortest and longest movies.
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
shortest_movie = df.loc[df['Duration'].idxmin(), ['Titles', 'Genre', 'Duration']]
longest_movie = df.loc[df['Duration'].idxmax(), ['Titles', 'Genre', 'Duration']]
st.subheader("8 : Shortest and Longest Movies")
st.write("Below are the shortest and longest movies based on their duration:")
movie_df = pd.DataFrame([shortest_movie, longest_movie])
st.table(movie_df)

#9: Use a heatmap to compare average ratings across genres.
df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
avg_ratings_per_genre = df.groupby('Genre', as_index=True)['Ratings'].mean().to_frame()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(avg_ratings_per_genre, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f", ax=ax)
ax.set_title("Heatmap of Average Ratings Across Genres (EDA)")
ax.set_xlabel("Genres")
ax.set_ylabel("Ratings")
st.subheader("9 : Heatmap of Average Ratings by Genre")
st.pyplot(fig)


#10: relationship between ratings and voting counts using a scatter plot
df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
df['Voatings'] = df['Voatings'].astype(str).str.replace('K', '000').str.extract(r'(\d+)')
df['Voatings'] = pd.to_numeric(df['Voatings'], errors='coerce').fillna(0)
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=df['Ratings'], y=df['Voatings'], hue=df['Genre'], size=df['Voatings'], sizes=(10, 200), palette="coolwarm", ax=ax)
ax.set_title("Relationship Between Ratings and Voting Counts (EDA)")
ax.set_xlabel("IMDb Ratings")
ax.set_ylabel("Voting Counts")
plt.grid(True)
st.subheader("10 : Scatter Plot - Ratings vs. Voting Counts")
st.pyplot(fig)




