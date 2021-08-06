from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
from time import sleep

import os

import requests

BASE_URL = 'https://www.hltv.org'
PLAYER_STATS = 'https://www.hltv.org/stats/players'
TEAM_STATS = 'https://www.hltv.org/stats/teams/'


def get_player_list():

    f = []

    raw = requests.get(PLAYER_STATS).text
    soup = BeautifulSoup(raw, 'html.parser')

    players = soup.find_all('td', {'class': 'playerCol'})

    for p in players:
        f.append({p.text: p.a['href']})

    return f


def get_team_list():
    f = []

    raw = requests.get(TEAM_STATS).text
    soup = BeautifulSoup(raw, 'html.parser')

    teams = soup.find_all('td', {'class': 'teamCol-teams-overview'})

    for t in teams:
        f.append({t.text: t.a['href']})

    return f



def get_player(name, player_list):

    plink = BASE_URL

    for p in player_list:

        if list(p.items())[0][0] == name:
            plink += p[name]
            break
    
    if plink == BASE_URL:
        return None

    raw = requests.get(plink).text
    soup = BeautifulSoup(raw, 'html.parser')

    stat_keys = map(lambda s: s.b.text, soup.find_all('div', {'class': 'summaryStatBreakdownSubHeader'}))
    stat_values = map(lambda s: s.text, soup.find_all('div', {'class': 'summaryStatBreakdownDataValue'}))

    return dict(zip(stat_keys, stat_values))

    


def get_team(name, team_list):
    plink = BASE_URL

    for t in team_list:

        if list(t.items())[0][0] == name:
            plink += t[name]
            break
    
    if plink == BASE_URL:
        return None

    raw = requests.get(plink).text
    soup = BeautifulSoup(raw, 'html.parser')

    stat_keys = map(lambda s: s.text, soup.find_all('div', {'class': 'small-label-below'}))
    stat_values = map(lambda s: s.text, soup.find_all('div', {'class': 'large-strong'}))

    return dict(zip(stat_keys, stat_values))

def reformat(name_list, func):

    f = []
    c = 1
    for n in name_list:
        
        print(f'Object {c} / {len(name_list)}')

        nm = list(n.items())[0][0]
        f.append(dict(list({'name': nm}.items()) + list(func(nm, name_list).items())))

        sleep(2)
        c += 1
    return f


def update_to_db():
    load_dotenv()

    client = MongoClient(os.environ['DB_CONNECT'])
    db = client['Stats']

    team_collection = db['Teams']
    player_collection = db['Players']

    team_stats = reformat(get_team_list(), get_team)
    player_stats = reformat(get_player_list(), get_player)

    for t in team_stats:
        if team_collection.find_one({'name': t['name']}) == None:
            team_collection.insert_one(t)
        else:
            team_collection.replace_one({'name': t['name']}, t)

    for p in player_stats:
        if team_collection.find_one({'name': p['name']}) == None:
            player_collection.insert_one(p)
        else:
            player_collection.replace_one({'name': p['name']}, t)
