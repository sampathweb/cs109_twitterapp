import os

class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATASETS = os.path.abspath(os.path.join(BASE_DIR, '..', 'datasets'))

class ProdConfig(Config):
    SECRET_KEY = 'CS109 - Final Project - What does data tell?'

class DevConfig(Config):
    SECRET_KEY = 'CS109 - Final Project - dev'
    DEBUG = True
