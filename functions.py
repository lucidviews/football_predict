import requests
import pandas as pd
from pprint import pprint
import json
import datetime

header_params = {
            'x-rapidapi-key': "848eec715emsh5f15e8bc1776ee0p1826d1jsn93d8284e8db5",
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


def get_standings(team_id):
    """
    Gets the current position of a team in the league it is playing in.

    Args:
        team_id (int): API-Football team ID.

    Returns:
        integer: An integer indicating the position in the league.
    """    
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    
    year = datetime.datetime.now().year

    querystring = {"season":str(year-1),"team":str(team_id)}

    response = requests.request("GET", url, headers=header_params, params=querystring)
    
    data = json.loads(response.text)
    
    return data['response'][0]['league']['standings'][0][0]['rank']


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
                       d['goals']['away']] for d in data['response'])
    df = df.rename(columns={0:'home_team', 1:'away_team', 2:'date', 3:'home_goals', 4:'away_goals'})
    
    return df


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
    Gets the satrting line up of the last game a team has palyed.

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

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    return data['response'][0]['predictions']


def top_scorer_assits(team_id):

