import csv

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from basketball_reference_web_scraper.data import Team


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
new_headers = ["minutes_pg", "start_percentage", "field_goal_per", "free_throw_per", "rebounds", "ATO", "steals_pg", "rebounds_pg", "assists_pg", "blocks_pg", "points_pg"]
season_headers_sorted = [
'slug',
'name',
'positions',
'age',
'team',
'games_played',
'games_started',
'start_percentage',
'minutes_pg',
'minutes_played',
'points',
'points_pg',
'field_goal_per',
'made_field_goals',
'attempted_field_goals',
'made_three_point_field_goals',
'free_throw_per',
'made_free_throws',
'attempted_free_throws',
'rebounds',
'rebounds_pg',
'assists',
'assists_pg',
'steals',
'steals_pg',
'blocks',
'blocks_pg',
'ATO'
]


def get_season_totals(year):
    return client.players_season_totals(season_end_year=year)


def get_advanced_season_totals(year):
    return client.players_advanced_season_totals(season_end_year=year)


def normalize_data(data):
    new_data = [data[0]]

    for i, row in enumerate(data, start=1):
        # if current row is equal to previous row's player
        found = False
        for x in range(len(new_data)):
            if new_data[x]["slug"] == row["slug"]:
                found = True
                prev_data = new_data[x]

                # for each column, aggregate data
                for header in csv_headers_season:
                    previous_value = prev_data[header]

                    # sum data with found
                    if header != "name" and header != "slug" and header != "team" and header != "positions" and header != "age":
                        new_data[x][header] = previous_value + row[header]

        if not found:
            new_data.append(row)

    return new_data


def calculate_percentages(data):
    for row in data:
        row["minutes_pg"] = round((row["minutes_played"] / row["games_played"]), 2) if (row["games_played"] > 0) else 0
        row["start_percentage"] = round((row["games_started"] / row["games_played"]), 2) if (row["games_played"] > 0) else 0
        row["field_goal_per"] = round((row["made_field_goals"] / row["attempted_field_goals"]), 2) if (row["attempted_field_goals"] > 0) else 0
        row["free_throw_per"] = round((row["made_free_throws"] / row["attempted_free_throws"]), 2) if (row["attempted_free_throws"] > 0) else 0
        row["rebounds"] = row["offensive_rebounds"] + row["defensive_rebounds"]
        row["ATO"] = round((row["assists"] / row["turnovers"]), 2) if (row["turnovers"] > 0) else row["assists"]

        row["steals_pg"] = round((row["steals"] / row["games_played"]), 2) if (
                    row["games_played"] > 0) else 0
        row["rebounds_pg"] = round((row["rebounds"] / row["games_played"]), 2) if (
                    row["games_played"] > 0) else 0
        row["assists_pg"] = round((row["assists"] / row["games_played"]), 2) if (
                    row["games_played"] > 0) else 0
        row["blocks_pg"] = round((row["blocks"] / row["games_played"]), 2) if (
                    row["games_played"] > 0) else 0
        row["points_pg"] = round((row["points"] / row["games_played"]), 2) if (
                row["games_played"] > 0) else 0

    return data


def write_data_obj_to_csv(data_to_write, headers):
    with open("player_data.csv", 'w', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, dialect='excel', extrasaction='ignore')
        writer.writeheader()

        for row in data_to_write:
            writer.writerow(row)


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


json_data = get_season_totals(2019)
normalized = normalize_data(json_data)
add_columns = calculate_percentages(normalized)
write_data_obj_to_csv(add_columns, season_headers_sorted)
