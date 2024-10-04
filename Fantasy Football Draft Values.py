import pandas as pd

df = pd.read_csv('FantasyPros_Fantasy_Football_Projections_FLX.csv')

adp_df = pd.read_csv('FantasyPros_2024_Overall_ADP_Rankings.csv')

adp_df['ADP Rank'] = adp_df['Current ADP'].rank()

adp_df_cutoff = adp_df[:100]

adp_df_cutoff.shape

# initialize an empty dictionary
replacement_players = {
    'RB': '',
    'QB': '',
    'WR': '',
    'TE': ''
}

for _, row in adp_df_cutoff.iterrows():
    
    position = row['Pos']  # extract out the position and player value from each row as we loop through it
    player = row['Player']
    
    if position in replacement_players: # if the position is in the dict's keys
        replacement_players[position] = player # set that player as the replacement player

replacement_values = {} # initialize an empty dictionary

for position, player_name in replacement_players.items():
    player = df.loc[df['Player'] == player_name.strip()]   
    replacement_values[position] = player['FantasyPoints'].tolist()[0]        

df['VOR'] = df.apply(
    lambda row: row['FantasyPoints'] - replacement_values.get(row['Pos']), axis=1 # grab each rows fantasy points and subtract replacement value
)

pd.set_option('display.max_rows', None) # turn off truncation of rows setting inherent to pandas

df['VOR Rank'] = df['VOR'].rank(ascending=False)

df = df.sort_values(by='VOR', ascending=False)

adp_df = adp_df.drop('Team', axis=1)

final_df = df.merge(adp_df, how='left', on=['Player', 'Pos']) # merge two data sets

# calculate the difference between value rank and adp rank
final_df['Diff in ADP and VOR'] = final_df['ADP Rank'] - final_df['VOR Rank']

draft_pool = final_df.sort_values(by='ADP Rank', ascending=True)[:200]

# Export the data to a CSV file
draft_pool.to_csv('Draft Values.csv', index=False)







