import pandas as pd
import sqlite3
# get elo csv from https://projects.fivethirtyeight.com/nba-model/nba_elo.csv

# get nba_elo.csv from the Datasets directory
def get_elo(url):
    elo = pd.read_csv('https://projects.fivethirtyeight.com/nba-model/nba_elo.csv')
    # elo = pd.read_csv('../../Datasets/nba_elo.csv')
    elo['date'] = pd.to_datetime(elo['date'])
    elo['date'] = elo['date'].dt.strftime('%Y-%m-%d')
    # replace abbreviations with full team names
    elo['team1'] = elo['team1'].replace({
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'LAC': 'LA Clippers',
        'LAL': 'Los Angeles Lakers',
        'PHO': 'Phoenix Suns',
        'SAC': 'Sacramento Kings',
        'DAL': 'Dallas Mavericks',
        'MEM': 'Memphis Grizzlies',
        'NOP': 'New Orleans Pelicans',
        'SAS': 'San Antonio Spurs',
        'ATL': 'Atlanta Hawks',
        'CHO': 'Charlotte Hornets',
        'MIA': 'Miami Heat',
        'ORL': 'Orlando Magic',
        'WAS': 'Washington Wizards',
        'BOS': 'Boston Celtics',
        'BRK': 'Brooklyn Nets',
        'NYK': 'New York Knicks',
        'PHI': 'Philadelphia 76ers',
        'TOR': 'Toronto Raptors',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DET': 'Detroit Pistons',
        'IND': 'Indiana Pacers',
        'MIL': 'Milwaukee Bucks',
        'DEN': 'Denver Nuggets',
        'MIN': 'Minnesota Timberwolves',
        'OKC': 'Oklahoma City Thunder',
        'POR': 'Portland Trail Blazers',
        'UTA': 'Utah Jazz'
    })
    elo['team2'] = elo['team2'].replace({
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'LAC': 'LA Clippers',
        'LAL': 'Los Angeles Lakers',
        'PHO': 'Phoenix Suns',
        'SAC': 'Sacramento Kings',
        'DAL': 'Dallas Mavericks',
        'MEM': 'Memphis Grizzlies',
        'NOP': 'New Orleans Pelicans',
        'SAS': 'San Antonio Spurs',
        'ATL': 'Atlanta Hawks',
        'CHO': 'Charlotte Hornets',
        'MIA': 'Miami Heat',
        'ORL': 'Orlando Magic',
        'WAS': 'Washington Wizards',
        'BOS': 'Boston Celtics',
        'BRK': 'Brooklyn Nets',
        'NYK': 'New York Knicks',
        'PHI': 'Philadelphia 76ers',
        'TOR': 'Toronto Raptors',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DET': 'Detroit Pistons',
        'IND': 'Indiana Pacers',
        'MIL': 'Milwaukee Bucks',
        'DEN': 'Denver Nuggets',
        'MIN': 'Minnesota Timberwolves',
        'OKC': 'Oklahoma City Thunder',
        'POR': 'Portland Trail Blazers',
        'UTA': 'Utah Jazz'
    })
    return elo

# Combine elo data with the data from the dataset
def add_elo(data, elo):
    merge_keys = ['TEAM_NAME', 'TEAM_NAME.1', 'Date']
    elo_columns = ['raptor_prob1', 'raptor_prob2', 'elo_prob1', 'elo_prob2', 'importance', 'team1', 'team2', 'date']
    merged_data = pd.merge(data, elo[elo_columns], left_on=merge_keys, right_on=['team1', 'team2', 'date'], how='left')
    merged_data = merged_data.rename(columns={'raptor_prob1': 'raptor_prob', 'raptor_prob2': 'raptor_prob.1', 'elo_prob1': 'elo_prob', 'elo_prob2': 'elo_prob.1'})
    merged_data = merged_data.drop(columns=['team1', 'team2', 'date'])
    return merged_data
    
# get dataset from Data/dataset.sqlite
def get_dataset():
    con = sqlite3.connect('../../Data/dataset.sqlite')
    df = pd.read_sql_query('select * from "dataset_2012-23"', con, index_col='index')
    # set date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df

def create_data():
    data = get_dataset()
    elo = get_elo('https://projects.fivethirtyeight.com/nba-model/nba_elo.csv')
    combined = add_elo(data, elo)
    combined.drop_duplicates(inplace=True)
    combined.to_csv('../../Datasets/dataset.csv')
    # combined.to_sql('dataset', con=sqlite3.connect('../../Data/dataset.sqlite'), if_exists='replace')

def update_dataset():
    elo = get_elo('https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv')
    data = get_dataset()
    combined = add_elo(data, elo)
    combined.drop_duplicates(inplace=True)
    combined.to_csv('../../Datasets/dataset2.csv', mode='w')
    combined.to_sql('dataset_elo', con=sqlite3.connect('../../Data/dataset.sqlite'), if_exists='replace')
update_dataset()

# TODO: include raptor data
# TODO: Test retraining
# TODO: Add more models
# TODO: Feature engineering
