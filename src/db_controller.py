
def generate_teams(stats, teams_data, force=False):
    temp_stats = stats.copy()
    teams = {}

    for item in teams_data:
        temp = Team(owner=item["owner"])

        for player in item["players"]:
            temp_stats = temp.add_player(player, temp_stats, force)
        teams[item["owner"]] = temp

    return teams, temp_stats


def add_player(team_name, teams, player, df):
    new_df = teams[team_name].add_player(player, df)
    new_df.to_csv("./database/projected_data.csv", index=False)

    teams_json = []
    for team in teams.keys():
        teams_json.append(teams[team].data_to_json())

    f = open("./database/teams_data.json", "w")
    f.write(json.dumps(teams_json))
    f.close()


def reset_database():
    stats_projected = read_projected()
    add_zscores(stats_projected)
    projected_copy = stats_projected.copy()

    # read team data
    with open("./data/teams_data.json") as f:
        team_data = json.loads(f.read())
        f.close()

    teams, projected_copy = generate_teams(projected_copy, team_data)

    teams_json = []
    for team in teams.keys():
        teams_json.append(teams[team].data_to_json())

    f = open("./database/teams_data.json", "w")
    f.write(json.dumps(teams_json))
    f.close()

    projected_copy.to_csv("./database/projected_data.csv", index=False)



def test_db(index):
    stats_projected = read_projected()
    add_zscores(stats_projected)
    projected_copy = stats_projected.copy()

    fake_team_data = []

    for x in range(1, 13):
        if x == index:
            fake_team_data.append({"owner": "Trent", "players": []})
        else:
            fake_team_data.append(gen_fake_team(x))

    teams, projected_copy = generate_teams(projected_copy, fake_team_data)

    teams_json = []
    for team in teams.keys():
        teams_json.append(teams[team].data_to_json())

    f = open("./database/teams_data.json", "w")
    f.write(json.dumps(teams_json))
    f.close()

    projected_copy.to_csv("./database/projected_data.csv", index=False)