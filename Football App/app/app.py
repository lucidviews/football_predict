import streamlit as st
import requests
import json
import functions as ft

def line_ups():
    df1 = ft.get_starting_11(team1_id)
    df2 = ft.get_starting_11(team2_id)

    with col1:
        for i in df1['player_id']:
            st.image(ft.get_photo(i), width=100)
    with col4:
        for i in df2['player_id']:
            st.image(ft.get_photo(i), width=100)

st.markdown(
"""
<style>
.reportview-container {
    background: url("https://wallpapercave.com/wp/FZauxCv.jpg");
    background-size: cover;
}
.sidebar .sidebar-content {
    background: url("https://wallpapercave.com/wp/FZauxCv.jpg");
    background-size: cover;
}
</style>
""",
unsafe_allow_html=True
)

col1, col2, col3 = st.beta_columns([70,200,30])
with col2:
    st.title('FOOTBALL PREDICTOR')
st.write("###")
st.write("###")

#bundesliga = ("Borussia Dortmund", "RB Leipzig", "Vfl Wolfsburg", "Bayern Munich", "FC Schalke 04", "Eintracht Frankfurt", "Werder Bremen", "VfB Stuttgart", "Hertha Berlin", "Borussia Mönchengladbach", "Union Berlin", "Bayer Leverkusen", "Arminia Bielefeld", "FSV Mainz 05", "SC Freiburg", "TSG Hoffenheim", "FC Köln", "FC Augsburg")
#team1 = st.sidebar.selectbox('Select Team 1', bundesliga)
#team2 = st.sidebar.selectbox('Select Team 2', bundesliga)

team1 = st.sidebar.text_input('Select Team 1', 'Borussia Dortmund')
team2 = st.sidebar.text_input('Select Team 1', 'Eintracht Frankfurt')

team1_id = ft.get_team_id(team1)
team2_id = ft.get_team_id(team2)

pred = ft.predictions(team1_id, team2_id)

col1, col2, col3, col4= st.beta_columns([50,18,62,20])
with col1:
    ft.get_logo(team1)
with col2:
    st.write("###")
    st.write('Winner:')
with col3:
    st.write("###")
    st.write(pred['winner']['name'])
with col4:
    ft.get_logo(team2)

st.write("###")
col1, col2, col3, col4 = st.beta_columns([50,18,62,20])
with col3:
    if st.button("Line-ups"):
        line_ups()