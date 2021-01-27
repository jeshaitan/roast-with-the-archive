import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'unknowableroast'
    FLASKS3_BUCKET_NAME = os.environ.get('FLASKS3_BUCKET_NAME') or 'roastgpt2models'
