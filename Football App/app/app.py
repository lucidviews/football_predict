import streamlit as st
import requests
import json
import functions as ft

#@st.cache(suppress_st_warning=True)
def line_ups():
    df1 = ft.get_starting_11(team1_id)
    df2 = ft.get_starting_11(team2_id)
    with col1:
        for i in range(len(df1['player_id'])):
            st.image(ft.get_photo(df1.iloc[i, 0]), width=100)
            st.write(df1.iloc[i, 1])
            st.write('Pos: ', df1.iloc[i, 2])
            st.write('No.: ', str(df1.iloc[i, 3]))
            st.write("###")
    with col3:
        for i in range(len(df2['player_id'])):
            st.image(ft.get_photo(df2.iloc[i, 0]), width=100)
            st.write(df2.iloc[i, 1])
            st.write('Pos: ', df2.iloc[i, 2])
            st.write('No.: ', str(df2.iloc[i, 3]))
            st.write("###")

def injured_players():
    df1 = ft.get_injured_player(team1_id)
    df2 = ft.get_injured_player(team2_id)
    with col1:
        if df1.empty:
            st.write('**No injuries are known!**')
        else:
            for i in range(len(df1['player_id'])):
                st.image(ft.get_photo(df1.iloc[i, 0]), width=100)
                st.write(df1.iloc[i, 1])
                st.write('Status: ', df1.iloc[i, 2])
                st.write("###")
    with col3:
        if df2.empty:
            st.write('**No injuries are known!**')
        else:
            for i in range(len(df2['player_id'])):
                st.image(ft.get_photo(df2.iloc[i, 0]), width=100)
                st.write(df2.iloc[i, 1])
                st.write('Status: ', df2.iloc[i, 2])
                st.write("###")
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

col1, col2, col3 = st.beta_columns([20,80,20])
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

col1, col2, col3= st.beta_columns([50,60,30])
with col1:
    st.write('_Home Win:_ ', pred['percent']['home'])
    ft.get_logo(team1)
    st.write("###")
with col2:
    st.write('_Draw_: ', pred['percent']['draw'])
    st.write("###")
    st.write('_Predicted Winner_:')
    st.write(pred['winner']['name'])

with col3:
    st.write('_Away Win_: ', pred['percent']['away'])
    ft.get_logo(team2)
    st.write("###")

st.write("###")
with col2:
    st.write("###")
    info = st.radio(
        'Show me',
        ('Line-ups', 'Injured Players', 'Head 2 Head')
    )
    if info == 'Line-ups':
        line_ups()
    elif info == 'Injured Players':
        injured_players()
    elif info == 'Head 2 Head':
        with col1:
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            df =ft.get_h2h(team1_id, team2_id)
            st.table(df.drop(columns=['home_goals', 'away_goals', 'date'], axis=1))