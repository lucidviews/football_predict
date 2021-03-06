import requests
import pandas as pd
from pprint import pprint
import json
import datetime
import numpy as np
import streamlit as st

header_params = {
            'x-rapidapi-key': "ENTER VALID KEY",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
            }

def get_team_id(team):    
    """
    Gets the API-Football team ID of a certain team.

    Args:
        team (string): The complete API-Football name of a certain football team. 

    Returns:
        integer: API-Football team ID.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"name":team}

    response = requests.request("GET", url, headers=header_params, params=querystring)

    data = json.loads(response.text)
    
    return data['response'][0]['team']['id']


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


def get_team_performance(team_id, season='2020'):
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

    dict = {'rank': data['response'][0]['league']['standings'][0][0]['rank'],
            'league': data['response'][0]['league']['standings'][0][0]['group'],
            'points': data['response'][0]['league']['standings'][0][0]['points'],
            'form': data['response'][0]['league']['standings'][0][0]['form'],
    }
    
    return dict


def get_standings_over_time(team_id, seasons=['2020', '2019', '2018', '2017', '2016']):
    """
    Calls the get_standings function for one or multiple times and stores the results in a dict.

    Args:
        team_id (integer): API-Football team ID.
        seasons (list, optional): Determines the different seasons for which the get_standings function is called. Defaults to ['2020', '2019', '2018', '2017', '2016'].

    Returns:
        dict: Contains a season as a key and a team's league rank in this season as a value.
    """    
    dict = {}
    for season in seasons:
        dict[season] = get_standings(team_id, season)

    return dict


def get_h2h(team_id_1, team_id_2):    
    """
    Gets the results of all last fixtures between two teams.

    Args:
        team_id_1 (integer): API-Football team ID.
        team_id_2 (integer): API-Football team ID.

    Returns:
        DataFrame: Contains the names of the home and the away team as well as the number of goals each team scored and the date of the fixture.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"

    h2h_string = str(team_id_1)+'-'+str(team_id_2)

    querystring = {"h2h":h2h_string}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)

    df = pd.DataFrame([d['teams']['home']['name'], 
                       d['teams']['away']['name'],
                       d['fixture']['date'],
                       d['goals']['home'],
                       d['goals']['away'],
                       d['league']['name'],
                       d['league']['season'],
                       d['fixture']['venue']['name']] for d in data['response'])
    df = df.rename(columns={0:'Home Team', 1:'Away Team', 2:'date', 3:'home_goals', 4:'away_goals', 5:'League', 6:'Season', 7:'Stadium'})
    df = df.dropna()
    df = df.astype({'home_goals':np.int8})
    df = df.astype({'away_goals':np.int8})
    df['Result'] = df['home_goals'].map(str)+':'+df['away_goals'].map(str)
    df = df.sort_values(by=['date'], ascending=False)
    df['Date'] = df['date'].apply(lambda x: x.split('T')[0])
    return df.reset_index(drop=True).head()


def get_injured_player(team_id, date=datetime.date.today()):
    """
    Gets all players of a team who are currently(!) injured.

    Args:
        team_id (integer): API-Football team ID.
        date (date, optional): Defaults to datetime.date.today() and therefore to today's date. If changed, the function returns all injured players at this date instead of the current ones.

    Returns:
        DataFrame: Contains the injiured players' ID, name, status, and a link to their picture.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/injuries"

    querystring = {'date':str(date), 'team':str(team_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)

    df = pd.DataFrame([d['player']['id'], 
                       d['player']['name'], 
                       d['player']['type'], 
                       d['player']['photo']] for d in data['response'])
    df = df.rename(columns={0:'player_id', 1:'player', 2:'status', 3:'photo_link'})

    return df


def get_starting_11(team_id):
    """
    Gets the starting line up of the last game a team has played.

    Args:
        team_id (integer): API-Football team ID.

    Returns:
        DataFrame: Contains each palyers' ID, name, position, and jersey number.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups"

    fixture_id = _get_last_fixture_ids(team_id, 1)

    querystring = {"team":str(team_id), 'fixture':str(fixture_id[0])}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)
    
    df = pd.DataFrame([d['player']['id'], d['player']['name'], d['player']['pos'], d['player']['number']] for d in data['response'][0]['startXI'])
    df = df.rename(columns={0:'player_id', 1:'player', 2:'position', 3:'jersey_number'})
    df = df.replace({'G':'Goalkeeper', 'D': 'Defender', 'M': 'Midfielder', 'F':'Forward'})

    return df


def _get_fixture_id_h2h(team_id_1, team_id_2, next=True):
    """
    Gets the API-Football fixture ID of either the last or the next fixture of a certain team.

    Args:
        team_id_1 (integer): API-Football team ID.
        team_id_2 (integer): API-Football team ID.
        next (bool, optional): Specifies whether the last (if next!=True) or the next (if next=True) fixture's ID of a certain team is returned. Defaults to True.

    Returns:
        integer: API-Football fixture ID.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"
    
    h2h_string = str(team_id_1)+'-'+str(team_id_2)

    if next==True:
        querystring = {"next":"1", 'h2h':h2h_string}
    else: 
        querystring = {"last":"1", 'h2h':h2h_string}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)  
    
    return data['response'][0]['fixture']['id']



def predictions(team_id_1, team_id_2):
    """
    Gets predictions for either the upcoming fixture or, if there is no future fixture palnned yet, for the last fixture between two specified teams.

    Args:
        team_id_1 (integer): API-Football team ID.
        team_id_2 (integer): API-Football team ID.

    Returns:
        dictionary: contains information on the most probable result and percentages for home win, draw or away win.
    """    
    try:
        fixture_id = _get_fixture_id_h2h(team_id_1, team_id_2)
    except:
        print('using last fixture')
        fixture_id = _get_fixture_id_h2h(team_id_1, team_id_2, next=False)
    
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

    querystring = {"fixture":fixture_id}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)

    return data['response'][0]['predictions'], data['response'][0]['teams']['home']['id'], data['response'][0]['teams']['away']['id']


def get_photo(player_id):
    """
    Gets the photo of a certain player.

    Args:
        player_id (integer): API-Football team ID.

    Returns:
        url: URL that leads to the file containing a player's picture.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/players"

    querystring = {"id": player_id, "season": "2020"}

    headers = {
        'x-rapidapi-key': "eff8f82f7dmsh5acc88f9a56c302p1b47acjsnfe16ac64e984",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)

    return data['response'][0]['player']['photo']


def _get_last_fixture_ids(team_id, num_last_matches):
    """
    Gets one or more fixture IDs of a specified team.

    Args:
        team_id (integer): API-Football team ID.
        num_last_matches (integer): Defines the number of last fixture IDs that is returned.

    Returns:
        list: Contains one or many last fixture IDs of a team.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"last": str(num_last_matches), 'team': str(team_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)

    fixture_ids = [f['fixture']['id'] for f in data['response']]

    return fixture_ids


def _get_last_fixture_dates(team_id, num_last_matches):
    """
    Gets one or more fixture dates of a specified team.

    Args:
        team_id (integer): API-Football team ID.
        num_last_matches (integer): Defines the number of last fixture dates that is returned.

    Returns:
        list: Contains one or many last fixture dates of a team.
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"last": str(num_last_matches), 'team': str(team_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    data = json.loads(response.text)

    fixture_dates = [f['fixture']['date'] for f in data['response']]

    return fixture_dates


def get_logo(team_id):
    """
    Gets a team's logo and outputs it as a streamlit element.

    Args:
        team_id (integer): API-Football team ID.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"id": team_id}

    response = requests.request("GET", url, headers=header_params, params=querystring)

    data = json.loads(response.text)

    link = data['response'][0]['team']['logo']

    st.image(link, width=100)


def get_all_leagues(season='2020'):
    """
    Gets all leagues that the API is supporting in a specified season.

    Args:
        season (str, optional): Defines the season out of which all leagues are returned. Defaults to '2020'.

    Returns:
        dict: Contains league names as values and their corresponding IDs as values.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    querystring = {'season':season}

    response = requests.request("GET", url, headers=header_params, params=querystring)

    data = json.loads(response.text)
    
    leagues = {}

    for element in data['response']:
        leagues[element['league']['name']] = element['league']['id']

    return leagues


def get_teams_of_league(league_id, season='2020'):
    """
    Gets all teams that are associated with a specified league in a specified season.

    Args:
        league_id (integer): API-Football league ID.
        season (str, optional): Defines the season out of which all teams of a league will be returned. Defaults to '2020'.

    Returns:
        list: Contains all teams of a specified league in a specified season. 
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {'season':season, 'league':str(league_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)

    data = json.loads(response.text)
    
    teams = []

    for element in data['response']:
        teams.append(element['team']['name'])

    return teams
