import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import functions as ft

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

_, col2, _ = st.beta_columns([30, 200, 30])
with col2:
    st.title('FOOTBALL PREDICTOR')
st.write("###")
st.write("###")

bundesliga = ("Borussia Dortmund", "RB Leipzig", "Vfl Wolfsburg", "Bayern Munich", "FC Schalke 04", "Eintracht Frankfurt", "Werder Bremen", "VfB Stuttgart", "Hertha Berlin", "Borussia Mönchengladbach", "Union Berlin", "Bayer Leverkusen", "Arminia Bielefeld", "FSV Mainz 05", "SC Freiburg", "TSG Hoffenheim", "FC Köln", "FC Augsburg")

team1 = st.sidebar.selectbox('Select Team 1', bundesliga)
team2 = st.sidebar.selectbox('Select Team 2', bundesliga)

header_params = {
            'x-rapidapi-key': "eff8f82f7dmsh5acc88f9a56c302p1b47acjsnfe16ac64e984",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
            }

def get_logo(team):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"name": team}

    response = requests.request("GET", url, headers=header_params, params=querystring)

    data = json.loads(response.text)

    link = data['response'][0]['team']['logo']

    st.image(link, width=100)

col1, col2, col3, col4 = st.beta_columns([25, 5, 30, 30])
with col1:
    get_logo(team1)
with col2:
    st.markdown("<h2 style='text-align: center; color: white;'>Score</h2>", unsafe_allow_html=True)
with col3:
    st.markdown("<h2 style='text-align: center; color: white;'>Score</h2>", unsafe_allow_html=True)
with col4:
    get_logo(team2)

def ronaldo():
    st.markdown("![Alt Text](https://i.giphy.com/media/8EoCZQ7lDDVKNMvNzL/giphy.gif)")
    return

st.write("###")
_, col2, _ = st.beta_columns(3)
with col2:
    if st.button("Press me"):
        ronaldo()