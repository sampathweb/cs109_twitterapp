#-------------------------------------------------------------------------------
# Name:        twitter recommender
# Purpose:      for cs109 call
#
# Author:      bconnaughton
#
# Created:     08/12/2013
# Copyright:   (c) bconnaughton 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from collections import defaultdict
import json

import matplotlib as mpl
# Force matplotlib to not use any Xwindows backend.
mpl.use('Agg')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
import matplotlib.cm as cm

#Specific for what is used below
# import oauth2 as oauth
import urlparse
import requests
import csv
from pattern import web

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB

from app.helpers import get_words_df

def main():
    pass

if __name__ == '__main__':
    main()

def make_xy(df, vectorizer=None):
    #Make bag of words, X is the count array, y is the columns
    if vectorizer is None:
        vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df.Tweet)
    X = X.tocsc()  # some versions of sklearn return COO format
    Y = (df.was_retweeted == True).values.astype(np.int)
    return X, Y

def log_likelihood(clf, x, y):
    prob = clf.predict_log_proba(x)
    rotten = y == 0
    fresh = ~rotten
    return prob[rotten, 0].sum() + prob[fresh, 1].sum()


def recommend(twitterword):
    newpd = get_words_df()
    # newpd = pd.read_csv('twitter_bigdf_appended_cleanedtweets_averageperuser.csv')
    newpd['Tweet'] = newpd['Tweet'].map(lambda x: str(x))

    newpd['was_retweeted'] = newpd['average_retweet_threshold']

    best_alpha = 50.0
    best_min_df = 0.01


    vectorizer = CountVectorizer(min_df=best_min_df)
    x, y = make_xy(newpd, vectorizer)
    xtrain, xtest, ytrain, ytest = train_test_split(x, y)

    clf = MultinomialNB(alpha=best_alpha).fit(xtrain, ytrain)

    probs = clf.predict_log_proba(x)[:, 0]

    prob = clf.predict_proba(x)[:, 0]
    predict = clf.predict(x)

    retweet_chance = abs(clf.predict_proba(vectorizer.transform([twitterword])) / probs.mean())

    answer = 'Compared to an average tweet, using "%s" in your tweet has the likliehood of a retweet of '%twitterword + str(retweet_chance[0][1])

    return answer



