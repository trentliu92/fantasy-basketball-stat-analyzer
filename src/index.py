def clear():
    lambda: os.system('clear')

def driver():
    clear()
    # read from csv

    # RESET
    # reset_database()

    # MOCK
    # test_db(3)
    # stats_projected = read_database()

    # MAIN RUN
    step = 0
    while step != 4:
        stats_projected = read_projected()
        add_zscores(stats_projected)

        teams_data = read_team()
        teams_dict, stats_projected = generate_teams(stats_projected, teams_data)

        team_list = []
        choice_dict = {}

        for i, team in enumerate(teams_dict.keys()):
            choice_dict[str(i + 1)] = team
            team_list.append(teams_dict[team])

        if step == 0:
            print("1. Print Suggestions")
            print("2. Add Players")
            step = int(input())

        if step == 1:
            clear()
            selection = {
                "points": {
                    "categories": ['PTS', 'AST', '3PM', 'STL'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "assists": {
                    "categories": ['AST', 'PTS', '3PM', 'STL'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "rebounds": {
                    "categories": ['REB', 'BLK', 'FG%', 'PTS'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "threes": {
                    "categories": ['3PM', 'PTS', 'STL', 'AST'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "blocks": {
                    "categories": ['BLK', 'REB', 'FG%', 'PTS'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "steals": {
                    "categories": ['STL', 'PTS', 'AST', '3PM'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "FGP": {
                    "categories": ['FGP', 'REB', 'BLK', 'PTS'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "FTP": {
                    "categories": ['FTP', 'PTS', 'AST', 'STL'],
                    "weights": [0.4, 0.25, 0.2, .15]
                },
                "DEF": {
                    "categories": ['BLK', 'STL', 'PTS'],
                    "weights": [0.4, 0.4, 0.2]
                }
            }

            for key in selection.keys():
                print(key)

            print("Select stat: ")
            sel_key = input()

            if len(teams_dict["Trent"].players) > 0:
                top_players_zscore(stats_projected, categories=['PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FT%', 'FG%'],
                                   weights=[.125 for i in range(8)], num_players=20)

                _ = calc_projected_score_percentile(stats_projected, team_list, showfig=True, color='team')
                simulate_top_picks(stats_projected, teams_dict["Trent"], categories=selection[sel_key]["categories"],
                                   weights=selection[sel_key]["weights"],
                                   num_players=10)
                step = 2
            else:
                print("Trent does not have enough players")
                step = 0

        if step == 2:
            for i, team in enumerate(teams_dict.keys()):
                print(str(i + 1) + ": " + team)

            # get team
            clear()
            print("Home")
            print("Exit")
            print("")
            print("Type index to get team:")

            team_choice = input()

            if team_choice == "Home" or team_choice == "home":
                step = 0
            elif team_choice == "Exit" or team_choice == "exit":
                step = 4
            else:
                int_choice = int(team_choice)
                pos = int(int_choice / 12)

                if pos % 2 == 1:
                    new_key = str(12 - (int_choice % 12) + 1)
                else:
                    new_key = str((int_choice % 12))

                team_key = choice_dict[new_key]
                # get player
                clear()
                print(team_key)
                print("Enter player name: ")
                player_name = input()
                player_name = player_name.strip()
                print(player_name)
                # add player
                add_player(team_key, teams_dict, player_name, stats_projected)


        clear()
        # print("continue?")
        # cont = input()
        #
        # if cont == "no":
        #     clear()
        #     step = 4
        #
        # clear()

if __name__ == '__main__':
    driver()