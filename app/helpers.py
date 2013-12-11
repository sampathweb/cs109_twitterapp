import pandas as pd
from flask import current_app

def get_viz_df(category, handle=None):
    if category == 'celebrity':
        filename = '/twitterusers_top_100_celebrity.csv'
    elif category == 'sports':
        filename = '/twitterusers_top_100_sports.csv'
    elif category == 'tech':
        filename = '/twitterusers_top_100_tech.csv'
    else:
        # Not extracted yet.  Need to create an empty data frame
        return pd.DataFrame()
    df = pd.read_csv(current_app.config['DATASETS'] + filename)
    if handle and handle[0] == '@':
        df = df[df['TwitterID'] == handle[1:]]
    if handle and handle[0] == '#':
        df = df[df['HashTag'] == handle[1:]]
    return df

def get_words_df():
    filename = '/twitter_bigdf_appended_cleanedtweets_averageperuser.csv'
    df = pd.read_csv(current_app.config['DATASETS'] + filename)
    return df

