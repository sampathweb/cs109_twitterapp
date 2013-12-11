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
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib as mpl

#Specific for what is used below
#import oauth2 as oauth
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

from sklearn.cross_validation import KFold

def cv_score(clf, x, y, score_func):
    """
    Uses 5-fold cross validation to estimate a score of a classifier

    Inputs
    ------
    clf : Classifier object
    x : Input feature vector
    y : Input class labels
    score_func : Function like log_likelihood, that takes (clf, x, y) as input,
                 and returns a score

    Returns
    -------
    The average score obtained by randomly splitting (x, y) into training and
    test sets, fitting on the training set, and evaluating score_func on the test set

    Examples
    cv_score(clf, x, y, log_likelihood)
    """
    result = 0
    nfold = 5
    for train, test in KFold(y.size, nfold): # split data into train/test groups, 5 times
        clf.fit(x[train], y[train]) # fit
        result += score_func(clf, x[test], y[test]) # evaluate score function on held-out data
    return result / nfold # average

def recommend(twitterword):
    newpd = get_words_df()
    # newpd = pd.read_csv('twitter_bigdf_useravg.csv')
    newpd['Tweet'] = newpd['Tweet'].apply(str)

    newpd['was_retweeted'] = newpd['average_retweet_threshold']

    X, Y = make_xy(newpd)

    xtrain, xtest, ytrain, ytest = train_test_split(X, Y)
    clf = MultinomialNB().fit(xtrain, ytrain)

    best_alpha = 50.0
    best_min_df = 0.01

    words = np.array(vectorizer.get_feature_names())

    x = np.eye(xtest.shape[1])
    probs = clf.predict_log_proba(x)[:, 0]
    ind = np.argsort(probs)

    good_words = words[ind[:10]]
    bad_words = words[ind[-10:]]

    good_prob = probs[ind[:10]]
    bad_prob = probs[ind[-10:]]

    return clf.predict_proba(vectorizer.transform([twitterword]))



