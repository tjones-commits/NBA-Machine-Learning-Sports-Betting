import pandas as pd
elo = pd.read_csv('../../Datasets/nba_elo_latest.csv')

# Return rows from the elo dataframe where the team with the higher elo rating had a higher score
def get_wins(elo):
    elo_wins = elo[elo['score1'] > elo['score2']]
    return wins

elo_pre_win = len(elo[(elo['elo1_pre'] > elo['elo2_pre']) & (elo['score1'] > elo['score2'])])
elo_pre_win += len(elo[(elo['elo1_pre'] < elo['elo2_pre']) & (elo['score1'] < elo['score2'])])

elo_prob_win = len(elo[(elo['elo_prob1'] > elo['elo_prob2']) & (elo['score1'] > elo['score2'])])
elo_prob_win += len(elo[(elo['elo_prob1'] < elo['elo_prob2']) & (elo['score1'] < elo['score2'])])

raptor_pre_win = len(elo[(elo['raptor1_pre'] > elo['raptor2_pre']) & (elo['score1'] > elo['score2'])])
raptor_pre_win += len(elo[(elo['raptor1_pre'] < elo['raptor2_pre']) & (elo['score1'] < elo['score2'])])

raptor_prob_win = len(elo[(elo['raptor_prob1'] > elo['raptor_prob2']) & (elo['score1'] > elo['score2'])])
raptor_prob_win += len(elo[(elo['raptor_prob1'] < elo['raptor_prob2']) & (elo['score1'] < elo['score2'])])

elo_raptor_wins = len(elo[((elo['elo_prob1'] > elo['elo_prob2']) & (elo['score1'] > elo['score2'])) | ((elo['elo_prob1'] < elo['elo_prob2']) & (elo['score1'] < elo['score2']))
                      & (((elo['raptor_prob1'] > elo['raptor_prob2']) & (elo['score1'] > elo['score2'])) | ((elo['raptor_prob1'] < elo['raptor_prob2']) & (elo['score1'] < elo['score2'])))])
print(F'total_games: {len(elo)}')
print(f'elo_pre_win: {elo_pre_win}')
print(f'elo_wins: {elo_raptor_wins}')
print(f'elo_prob_win: {elo_prob_win}')
print(f'raptor_pre_win: {raptor_pre_win}')
print(f'raptor_prob_win: {raptor_prob_win}')


