import streamlit as st
import numpy as np
import requests
import json
import itertools as it
import plotly.express as px
import functions as ft

# Setting the background picture of the app
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

# Get all leagues the API currently supports with their corresponding IDs in a dict with get_all_leagues()
leagues = ft.get_all_leagues()

# Creating a select box where the user can choose from all leagues that were pulled in the previous steps
# st.sidebar.write("###") is used to insert linebreaks 
league = st.sidebar.selectbox('Select League', list(leagues.keys()), index=list(leagues.keys()).index('Bundesliga 1'))
st.sidebar.write("###")
st.sidebar.write("###")

# Get league id from the league the user selected 
league_id = leagues[league]

# Get all teams that are in the league the user selected 
teams = ft.get_teams_of_league(league_id)

# Create select box where the user can select a team from the league he/she defined previously
team1 = st.sidebar.selectbox('Select Team 1', teams)
team2 = st.sidebar.selectbox('Select Team 2', teams, index=2)

# Pulling ids of teams based on sidebar selection with get_team_id()
team1_id = ft.get_team_id(team1)
team2_id = ft.get_team_id(team2)

# Definition of variables for prediciton + home and away team
pred, home_team, away_team = ft.predictions(team1_id, team2_id)

# Defining the column spacing the header of the application with three columns
col1, col2, col3 = st.beta_columns([20,80,20])
with col2:
    st.title('FOOTBALL PREDICTOR')
    st.write('## _{}_'.format(league))
st.write("###")
st.write("###")

# Pulling percentages of prediction for win, draw and loss 
# Implementation of animation to show winner with button
col1, col2, col3= st.beta_columns([50,50,50])
with col1:
    st.write('_Win_: ', pred['percent']['home'])
    ft.get_logo(home_team)
    st.write("###")
with col2:
    st.write('_Draw_: ', pred['percent']['draw'])
    st.write("###")
    if st.button('Show winner'):
        st.write(pred['winner']['name'])
        st.image('https://media2.giphy.com/media/jIRyzncqRWzM3GYaQm/giphy.gif', width=150)
with col3:
    st.write('_Win_: ', pred['percent']['away'])
    ft.get_logo(away_team)
    st.write("###")

# Adding radio buttons to the middle column for feature selection 
st.write("###")
with col2:
    st.write("###")
    info = st.radio(
        'Show me',
        ('Line-ups', 'Standings', 'Head 2 Head', 'Injured Players')
    )

    # Calling fucntions according to selected functionality
    if info == 'Line-ups':
        df1 = ft.get_starting_11(home_team)
        df2 = ft.get_starting_11(away_team)
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

    elif info == 'Head 2 Head':
        with col1:
            st.write("###")
            st.write("###")
            st.write("###")
            st.write("###")
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

            dict_team1 = ft.get_team_performance(home_team)
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

            dict_team2 = ft.get_team_performance(away_team)
            st.write('## Rank: ', dict_team2['rank'])
            st.write('## #Points: ', dict_team2['points'])
            st.write('## Form: ', dict_team2['form'])

    elif info == 'Injured Players':
        df1 = ft.get_injured_player(home_team)
        df2 = ft.get_injured_player(away_team)
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