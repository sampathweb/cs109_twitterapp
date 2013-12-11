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
    if handle:
        df = df[df['TwitterID'] == handle]
    return df

def get_words_df():
    filename = '/twitter_bigdf_useravg.csv'
    df = pd.read_csv(current_app['DATASETS'] + filename)
    return df

