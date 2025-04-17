import streamlit as st


page = st.sidebar.radio(label="Select a Page", options=['Data_Visualization', 'Filtration'])


if page == "Data_Visualization":
    st.title("Data Visualization")
    exec(open("E:\\IMDB_2024_Data_Scraping_and_Visualizations\\scraping\\Data_Visualization.py", encoding="utf-8").read())

elif page == "Filtration":
    st.title(" Filtration")
    exec(open("E:\\IMDB_2024_Data_Scraping_and_Visualizations\\scraping\\Filtration.py", encoding="utf-8").read())