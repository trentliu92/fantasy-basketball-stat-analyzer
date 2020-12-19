from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import csv

# from basketball_reference_web_scraper import client
#
csv_headers = [
    "slug",
    "name",
    "positions",
    "age",
    "team",
    "games_played" ,
    "minutes_played" ,
    "player_efficiency_rating",
    "true_shooting_percentage",
    "three_point_attempt_rate",
    "free_throw_attempt_rate",
    "offensive_rebound_percentage",
    "defensive_rebound_percentage",
    "total_rebound_percentage",
    "assist_percentage",
    "steal_percentage",
    "block_percentage",
    "turnover_percentage",
    "usage_percentage",
    "offensive_win_shares",
    "defensive_win_shares",
    "win_shares",
    "win_shares_per_48_minutes",
    "offensive_box_plus_minus",
    "defensive_box_plus_minus",
    "box_plus_minus",
    "value_over_replacement_player",
    "is_combined_totals"
]

csv_headers_season = [
'slug',
'name',
'positions',
'age',
'team',
'games_played',
'games_started',
'minutes_played',
'made_field_goals',
'attempted_field_goals',
'made_three_point_field_goals',
'attempted_three_point_field_goals',
'made_free_throws',
'attempted_free_throws',
'offensive_rebounds',
'defensive_rebounds',
'assists',
'steals',
'blocks',
'turnovers',
'personal_fouls',
'points'
]


def get_season_totals(year):
    return client.players_season_totals(season_end_year=year)


def get_advanced_season_totals(year):
    return client.players_advanced_season_totals(season_end_year=year)


def normalize_data(data):
    new_data = [data[0]]
    # print(data)
    for i, row in enumerate(data, start=1):
        # if current row is equal to previous row's player
        if data[len(new_data) - 1]["slug"] == row["slug"]:

            # for each column, aggregate data
            for header in csv_headers_season:
                previous_value = new_data[len(new_data) - 1][header]
                if header == "name" or header == "slug":
                    # do nothing
                    break
                elif header == "team":
                    new_data[len(new_data) - 1][header] = previous_value + " " + row[header]
                elif header == "positions":
                    new_data[len(new_data) - 1][header].append(row[header])
                else:
                    new_data[len(new_data) - 1][header] = previous_value + row[header]
            # end
        else:
            new_data.append(row)
    print(new_data)




            # writer.writerow(row[param])


def write_data_obj_to_csv(data):
    with open("player_data", 'w', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)

        for row in data:
            for i in range(len(headers)):
                param = headers[i]
                writer.writerow(row[param])


def season_totals_to_csv(season):
    next_season = season + 1
    client.players_season_totals(
        season_end_year=season,
        output_type=OutputType.CSV,
        output_file_path="./" + season + "_" + next_season + "_player_season_totals.csv"
    )


def advanced_season_totals_to_csv(season):
    next_season = season + 1
    client.players_advanced_season_totals(
        season_end_year=season,
        output_type=OutputType.CSV,
        output_file_path="./" + season + "_" + next_season + "_advanced_player_season_totals.csv"
    )


data = get_season_totals(2019)
normalize_data(data)
