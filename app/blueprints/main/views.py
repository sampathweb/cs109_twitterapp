from flask import Blueprint, render_template, session, redirect, url_for, request, abort
from flask import current_app, make_response

import datetime
import StringIO
import random
from collections import defaultdict
import json

import numpy as np
import pandas as pd
import scipy
import scipy.stats

import matplotlib as mpl
# Force matplotlib to not use any Xwindows backend.
mpl.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.cm as cm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from app.twitterword import recommend
from app.helpers import get_viz_df

main = Blueprint(
    'main', 
    __name__,
    template_folder='templates'
)

#colorbrewer2 Dark2 qualitative color table
dark2_colors = [(0.10588235294117647, 0.6196078431372549, 0.4666666666666667),
                (0.8509803921568627, 0.37254901960784315, 0.00784313725490196),
                (0.4588235294117647, 0.4392156862745098, 0.7019607843137254),
                (0.9058823529411765, 0.1607843137254902, 0.5411764705882353),
                (0.4, 0.6509803921568628, 0.11764705882352941),
                (0.9019607843137255, 0.6705882352941176, 0.00784313725490196),
                (0.6509803921568628, 0.4627450980392157, 0.11372549019607843)]

rcParams['figure.figsize'] = (10, 6)
rcParams['figure.dpi'] = 150
rcParams['axes.color_cycle'] = dark2_colors
rcParams['lines.linewidth'] = 2
rcParams['axes.facecolor'] = 'white'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'white'
rcParams['patch.facecolor'] = dark2_colors[0]
rcParams['font.family'] = 'StixGeneral'


def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks
    
    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    
    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    
    #now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()
        
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')    


@main.route('/explore/<category>/', methods=['GET', 'POST'])
def explore(category='sports'):
    handle = None
    if request.method == 'POST':
        handle = request.form.get('handle')
    if handle and (handle[0] != '@' and handle[0] != '#'):
        handle = None
    return render_template('main/explore.html', category=category, handle=handle)

@main.route('/words/', methods=['GET', 'POST'])
def words():
    search = ''
    word_score = None
    if request.method == 'POST':
        search = request.form.get('search')
    if search:
        word_score = recommend(search)
    return render_template('main/words.html', search=search, word_score=word_score)

@main.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')

@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

@main.route("/explore/<category>/<fig_type>/<fig_data>/viz_category.png/")
@main.route("/explore/<category>/<fig_type>/<fig_data>/viz_category.png/<handle>/")
def viz_category(category=None, handle=None, fig_type='hist', fig_data='retweet'):
    pd_tweets = get_viz_df(category, handle)
    png_output = StringIO.StringIO()
    fig = plt.figure()
    if fig_type == 'hist':
        if fig_data == 'retweet':
            plt.hist(pd_tweets.Retweet, bins=100, range=(0, 10000), log=True)
        elif fig_data == 'favorite':
            plt.hist(pd_tweets.Favorite, bins=100, range=(0, 10000), log=True)
    plt.savefig(png_output, dpi=150)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
