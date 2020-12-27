import json
import csv
import unidecode

stat_headers = ["Rank", "Name", "Gs", "MPG", "FGA", "FGM", "FG%", "FTA", "FTM", "FT%", "3PM", "REB", "AST", "ATO", "STL", "BLK", "TOV", "PTS"]
new_headers = ["FGA", "FGM", "FTA", "FTM"]


def read_csv(file_dir):
    with open(file_dir, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        temp_list = []
        for row in reader:
            temp_list.append(row)

        return temp_list



def write_data_obj_to_csv(data_to_write, headers):
    with open("player_data.csv", 'w', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, dialect='excel', extrasaction='ignore')
        writer.writeheader()

        for row in data_to_write:
            writer.writerow(row)


def write_data_obj_to_csv(data_to_write, headers):
    with open("projected_player_data.csv", 'w', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, dialect='excel', extrasaction='ignore')
        writer.writeheader()

        for row in data_to_write:
            writer.writerow(row)

def assign_new_averages(stats_new, stats_old):
    for player in stats_new:
        # find user
        res = list(filter(lambda person: unidecode.unidecode(person['Name']) == player["Name"], stats_old))

        fgp = float(player["FG%"])
        ftp = float(player["FT%"])

        if len(res) == 0:
            print(player["Name"])
            res = [{"FGM": 3.0, "FTM": 2.0, "FGA": 5.0, "FTA": 4.0}]

        for header in new_headers:
            if header == "FGM":
                new_header = round(fgp * float(res[0]["FGA"]), 2)
            elif header == "FTM":
                new_header = round(ftp * float(res[0]["FTA"]), 2)
            else:
                new_header = res[0][header]

            player[header] = new_header

    return stats_new


def fix_averages(stats_new):
    fix_players = [
        "Obi Toppin",
        "DeMarcus Cousins",
        "Killian Hayes",
        "James Wiseman",
        "Anthony Edwards",
        "Patrick Williams",
        "Deni Avdija",
        "Devin Vassell",
        "Aaron Nesmith",
        "Isaac Okoro",
        "Onyeka Okongwu",
        "Harry Giles III",
        "Terence Davis II",
        "Kira Lewis Jr.",
        "Cole Anthony",
        "Jalen Smith",
        "Saddiq Bey",
    ]

    for player in fix_players:
        # find user
        index = next((index for (index, d) in enumerate(stats_new) if d['Name'] == player), None)

        fgp = float(stats_new[index]["FG%"])
        ftp = float(stats_new[index]["FT%"])

        new_val = {"FGM": 3.0, "FTM": 2.0, "FGA": 6.5, "FTA": 1.1}

        stats_new[index]["FGM"] = round(fgp * float(new_val["FGA"]), 2)
        stats_new[index]["FTM"] = round(ftp * float(new_val["FTA"]), 2)
        stats_new[index]["FTA"] = new_val["FTA"]
        stats_new[index]["FGA"] = new_val["FGA"]

    return stats_new


def main():
    file_dir_projected = "./projected_player_data.csv"
    # file_dir_2019_2020 = "../data/online_19_20_stats.csv"

    stats_projected = read_csv(file_dir_projected)
    # stats_2019_2020 = read_csv(file_dir_2019_2020)

    # stats_projected = assign_new_averages(stats_projected, stats_2019_2020)

    stats_projected = fix_averages(stats_projected)

    write_data_obj_to_csv(stats_projected, stat_headers)



main()
