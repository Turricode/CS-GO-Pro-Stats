from bs4 import BeautifulSoup
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
        print(list(t.items())[0][0])
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


def update_to_db():
    pass

print(get_team('TYLOO', get_team_list()))