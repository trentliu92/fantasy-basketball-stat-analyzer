# very hacky way of parsing the top 250 players on the projected ESPN Fantasy Basketball Page

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import time
import csv

# define constants
stat_headers = ["Gs", "MPG", "FG%", "FT%", "3PM", "REB", "AST", "ATO", "STL", "BLK", "TOV", "PTS"]
player_headers = ["Rank", "Name"]
full_header = player_headers + stat_headers
url = 'https://fantasy.espn.com/basketball/players/projections'


def parse_html(html, first_rank):
    soup = BeautifulSoup(html, 'html.parser')

    # player names
    names = soup.find_all('div', {'class': 'player-name'})

    # stats
    games_played = soup.find_all('div', {'title': 'Games Played'})
    minutes = soup.find_all('div', {'title': 'Minutes'})
    field_goals = soup.find_all('div', {'title': 'Field Goal Percentage'})
    free_throws = soup.find_all('div', {'title': 'Free Throw Percentage'})
    three_pointers = soup.find_all('div', {'title': 'Three Pointers Made'})
    rebounds = soup.find_all('div', {'title': 'Rebounds'})
    assists = soup.find_all('div', {'title': 'Assists'})
    assists_to_turnovers = soup.find_all('div', {'title': 'Assists To Turnover Ratio'})
    steals = soup.find_all('div', {'title': 'Steals'})
    blocks = soup.find_all('div', {'title': 'Blocks'})
    turnovers = soup.find_all('div', {'title': 'Turnovers'})
    points = soup.find_all('div', {'title': 'Points'})

    total_stats = [games_played, minutes, field_goals, free_throws, three_pointers, rebounds, assists,
                   assists_to_turnovers, steals, blocks, turnovers, points]

    total_players = []

    for rank, player_name in enumerate(names):
        total_players.append({'Rank': first_rank + rank + 1, 'Name': player_name.text})

    for s, stats in enumerate(total_stats):
        for p, player_stat in enumerate(stats):
            if p != 0 and (p + 1) % 3 == 0:
                index = int((p + 1)/3 - 1)
                total_players[index][stat_headers[s]] = player_stat.text

    return total_players


def write_data_obj_to_csv(data_to_write, headers):
    with open("projected_player_data.csv", 'w', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, dialect='excel', extrasaction='ignore')
        writer.writeheader()

        for row in data_to_write:
            writer.writerow(row)


def init():
    # define chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver = os.getcwd() + "/chromedriver"

    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    driver.get(url)

    return driver


def main():
    driver = init()
    all_players = []

    for page in range(2, 7):
        time.sleep(5)
        html = driver.page_source

        first_rank = len(all_players)
        all_players += parse_html(html, first_rank)

        time.sleep(2)
        driver.find_element_by_id(str(page)).click()

    # print(all_players)
    write_data_obj_to_csv(all_players, full_header)


main()