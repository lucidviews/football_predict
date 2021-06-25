import streamlit as st
import numpy as np
import requests
import json
import itertools as it
import plotly.express as px
import functions as ft

#@st.cache(suppress_st_warning=True)
def get_standings(team_id, season='2020'):
    """
    Gets the current position of a team in the league it is playing in.

    Args:
        team_id (int): API-Football team ID.

    Returns:
        integer: An integer indicating the position in the league.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    
    year = datetime.datetime.now().year

    querystring = {"season":str(season),"team":str(team_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    
    data = json.loads(response.text)
    
    return data['response'][0]['league']['standings'][0][0]['rank']

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
    background: url("https://wallpapercave.com/wp/5DMx8Xb.jpg");
    background-size: cover;
}
.sidebar .sidebar-content {
    background: url("https://wallpapercave.com/wp/5DMx8Xb.jpg");
    background-size: cover;
}
</style>
""",
unsafe_allow_html=True
)

team1 = st.sidebar.text_input('Select Team 1', 'Borussia Dortmund')
team2 = st.sidebar.text_input('Select Team 2', 'Eintracht Frankfurt')

team1_id = ft.get_team_id(team1)
team2_id = ft.get_team_id(team2)

pred = ft.predictions(team1_id, team2_id)

col1, col2, col3 = st.beta_columns([20,80,20])
with col2:
    st.title('FOOTBALL PREDICTOR')
    st.write('## _{}_'.format(ft.get_team_performance(team1_id)['league']))
st.write("###")
st.write("###")

#bundesliga = ("Borussia Dortmund", "RB Leipzig", "Vfl Wolfsburg", "Bayern Munich", "FC Schalke 04", "Eintracht Frankfurt", "Werder Bremen", "VfB Stuttgart", "Hertha Berlin", "Borussia Mönchengladbach", "Union Berlin", "Bayer Leverkusen", "Arminia Bielefeld", "FSV Mainz 05", "SC Freiburg", "TSG Hoffenheim", "FC Köln", "FC Augsburg")
#team1 = st.sidebar.selectbox('Select Team 1', bundesliga)
#team2 = st.sidebar.selectbox('Select Team 2', bundesliga)

col1, col2, col3= st.beta_columns([50,50,50])
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
        ('Line-ups', 'Standings', 'Head 2 Head', 'Injured Players')
    )
    if info == 'Line-ups':
        line_ups()
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
    elif info == 'Standings':
        with col1:
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")

            dict_team1 = ft.get_team_performance(team1_id)
            st.write('## Rank: ', dict_team1['rank'])
            st.write('## #Points: ', dict_team1['points'])
            st.write('## Form: ', dict_team1['form'])

            st.write("###")
            st.write("###")

            dict_team1 = ft.get_standings_over_time(team1_id)
            dict_team2 = ft.get_standings_over_time(team2_id)

            fig = px.line(x=list(dict_team1.keys()), y=[list(dict_team1.values()), list(dict_team2.values())],
            labels={'value': 'Rank in League', 'x': 'Season', 'variable':'Teams'},
            title='Ranking Over Last 5 Seasons')
            fig.update_yaxes(range = [19, 1], tickvals=list(np.arange(1,19)), gridcolor='darkgray')
            fig.update_xaxes(autorange = 'reversed', tickangle = -30, gridcolor='darkgray')
            names = it.cycle([team1, team2])
            fig.for_each_trace(lambda t:  t.update(name = next(names)))
            st.plotly_chart(fig)

        with col3:
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")

            dict_team2 = ft.get_team_performance(team2_id)
            st.write('## Rank: ', dict_team2['rank'])
            st.write('## #Points: ', dict_team2['points'])
            st.write('## Form: ', dict_team2['form'])


    elif info == 'Injured Players':
        injured_players()