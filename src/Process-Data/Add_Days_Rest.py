import re
import sqlite3
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta

def get_date(date_string):
    # Get the year, month, and day from the date_string
    year1,month,day = re.search(r'(\d+)-\d+-(\d\d)(\d\d)', date_string).groups()
    # If the month is before September, add 1 to the year
    year = year1 if int(month) > 8 else int(year1) + 1
    # Return the date as a datetime object
    return datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')

# import packages
import sqlite3
import pandas as pd
from tqdm import tqdm

# set up connection
con = sqlite3.connect("../../Data/odds.sqlite")

# get all datasets in database
datasets = ["odds_2022-23", "odds_2021-22", "odds_2020-21", "odds_2019-20", "odds_2018-19", "odds_2017-18", "odds_2016-17", "odds_2015-16", "odds_2014-15", "odds_2013-14", "odds_2012-13", "odds_2011-12", "odds_2010-11", "odds_2009-10", "odds_2008-09", "odds_2007-08"]

# loop through datasets
for dataset in tqdm(datasets):
    # read data from dataset
    data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
    
    # create dictionary to hold last played date for each team
    teams_last_played = {}
    
    # loop through each row of data
    for index, row in data.iterrows():
        # skip row if home or away team is not in row
        if 'Home' not in row or 'Away' not in row:
            continue
        
        # if home team has not played yet, set number of games rested to 10 (start of season)
        if row['Home'] not in teams_last_played:
            teams_last_played[row['Home']] = get_date(row['Date'])
            home_games_rested = 10
        # if home team has played, set number of games rested to the difference between the current date and last played date
        else:
            current_date = get_date(row['Date'])
            home_games_rested = (current_date - teams_last_played[row['Home']]).days if 0 < (current_date - teams_last_played[row['Home']]).days < 9 else 9
            teams_last_played[row['Home']] = current_date
        
        # if away team has not played yet, set number of games rested to 10 (start of season)
        if row['Away'] not in teams_last_played:
            teams_last_played[row['Away']] = get_date(row['Date'])
            away_games_rested = 10
        # if away team has played, set number of games rested to the difference between the current date and last played date
        else:
            current_date = get_date(row['Date'])
            away_games_rested = (current_date - teams_last_played[row['Away']]).days if 0 < (current_date - teams_last_played[row['Away']]).days < 9 else 9
            teams_last_played[row['Away']] = current_date
        
        # update date
        data.at[index,'Days_Rest_Home'] = home_games_rested
        data.at[index,'Days_Rest_Away'] = away_games_rested

    # write data to db
    data.to_sql(dataset, con, if_exists="replace")

con.close()
