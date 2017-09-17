# -*- coding: utf-8 -*-

'''
sentiment_service.py
~~~~~~~~~~~~~~~~~~~~

App implements a sentiment analysis pipeline. 

'''

import cPickle as pickle
import pandas as pd
import requests
import json
import sys
import warnings
from springcloudstream.tcp.stream import Processor

warnings.filterwarnings("ignore")

resp = requests.get(
    "https://raw.githubusercontent.com/crawles/gpdb_sentiment_analysis_twitter_model/master/twitter_sentiment_model.pkl")
resp.raise_for_status()
cl = pickle.loads(resp.content)


def regex_preprocess(raw_tweets):
    tweets = map(lambda t: t['text'], raw_tweets)

    pp_text = pd.Series(tweets)

    user_pat = '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)'
    http_pat = '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    repeat_pat, repeat_repl = "(.)\\1\\1+", '\\1\\1'

    pp_text = pp_text.str.replace(pat=user_pat, repl='USERNAME')
    pp_text = pp_text.str.replace(pat=http_pat, repl='URL')
    pp_text.str.replace(pat=repeat_pat, repl=repeat_repl)
    return pp_text


def post_process(polarities, tweets):
    result = []
    try:
        for i, polarity in enumerate(polarities):
            result.append({'polarity': round(polarity,2), 'text': tweets[i]})

        return json.dumps(result)

    except:
        return json.dumps([])

def process(data):
    # Array of raw tweets
    raw_tweets = json.loads(str(data))
    # Convert to {[text1,text2,...]}
    tweets = regex_preprocess(raw_tweets)

    ## run the prediction
    prediction = cl.predict_proba(tweets)[:][:, 1]

    return post_process(prediction.tolist(),tweets)

import socket, logging

logging.info("socket.gethostname() %s" % socket.gethostname())
logging.info("ip long way %s" % [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
logging.info("ip socket.gethostname(socket.gethostname()) %s" % socket.gethostbyname(socket.gethostname()))
logging.info("ip for localhost %s" % socket.gethostbyname('localhost'))
Processor(process, sys.argv).start()