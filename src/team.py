import pandas as pd

# ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FG%', 'FT%', 'TOV']
class Team:
    def __init__(self, owner):
        self.owner = owner
        self.players = []

    def add_player(self, player, df, force=False):
        if len(self.players) > 13:
            print('Too many players.')
        elif df is None:
            print('No data frame was passed')
        elif not force and (not df.Name.isin([player]).any() or df.loc[df.Name.isin([player]), 'Taken'].item() == True):
            print(player + ' is not available.')
        else:
            self.players.append(player.strip())
            df.loc[df.Name.isin([player]), 'Taken'] = True
        return df

    def remove_player(self, player, df):
        self.players.remove(player.strip())
        df.loc[df.Name.isin([player]), 'Taken'] = False
        return df

    def calculate_projected_score(self, stats):
        data = stats[stats.Name.isin(self.players)]
        res = {}
        for col in ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'TOV']:
            res[col] = data[col].sum()
        res['FT%'] = data['FTM'].sum() / data['FTA'].sum()
        res['FG%'] = data['FGM'].sum() / data['FGA'].sum()
        res_df = pd.DataFrame(res, index=[self.owner])
        return res_df

    def show_roster(self):
        print(self.players)

    def data_to_json(self):
        return {"owner": self.owner, "players": self.players}