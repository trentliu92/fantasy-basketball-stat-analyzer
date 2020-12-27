
import pandas as pd
import json
import csv
# db definitions

# historical 2019-2020 season data
def read_19_20():
    stats_19_20 = pd.read_csv('./data/online_19_20_stats.csv')
    stats_19_20.drop('Rank', axis=1, inplace=True)
    stats_19_20['Taken'] = False
    return stats_19_20


# projected data scraped from ESPN
def read_projected():
    stats_projected = pd.read_csv('./data/projected_player_data.csv')
    stats_projected['Taken'] = False
    return stats_projected


def read_database():
    stats_db = pd.read_csv('./database/projected_data.csv')
    return stats_db


def read_team():
    with open("./database/teams_data.json") as f:
        team_data = json.loads(f.read())
        f.close()
        return team_data
