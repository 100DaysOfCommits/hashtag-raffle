import json

__author__ = 'lorenamesa'

import falcon
import requests
import os
import yaml
from itertools import groupby
import operator

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

api = application = falcon.API()


class TweetsProcessor(object):

    #  https://developers.google.com/sheets/reference/rest/v4/spreadsheets.values/get
    base_url = 'https://sheets.googleapis.com/v4/spreadsheets/{0}/values/{1}?key={2}'
    RETWEET = 'RT '

    def __init__(self):
        self.__set__state__()
        self.excluded_user_ids = ['745803139157266433', '2939981430', '2457141158', '4091328874']
        self.stop_words = ['RT']

    def __set__state__(self):
        with open("{0}/config.yml".format(BASE_DIR), 'r') as stream:
            doc = yaml.load(stream)
            self.api_key = doc.get('GOOGLE_SHEETS')
            self.spreadsheet_id = doc.get('SPREADSHEET_ID')

    def get_tweet_leaders(self):
        response = requests.get(self.base_url.format(self.spreadsheet_id, "A:D", self.api_key))
        if not response.ok:
            return (response.content, True)

        json = response.json().get('values')
        #  Headers 'Twitter User', 'Twitter User Id', 'Tweet Id', 'Text', 'Date'
        headers = json.pop(0)
        tweets = [dict(zip(headers, tweet)) for tweet in json]
        filtered_tweets = list(filter(lambda t: t.get('Twitter User Id') not in self.excluded_user_ids and self.RETWEET not in t.get('Text'), tweets))

        tweets_by_id = {}

        for tweet_id, group in groupby(filtered_tweets, lambda t: t.get('Twitter User')):
            tweets = set(map(lambda t: t.get('Tweet Id'), group))
            print(tweets)
            tweets_by_id[tweet_id] = len(tweets)

        return (sorted(tweets_by_id.items(), key=operator.itemgetter(0)), False)


class Resource(object):

    def on_get(self, req, resp):
        tweets, err = TweetsProcessor().get_tweet_leaders()

        if err:
            resp.status = falcon.HTTP_500
            resp.body = '{"message":"Internal server error, try again later."}'
            return resp

        resp.body = json.dumps(tweets)
        resp.status = falcon.HTTP_200
        return resp


leaders = Resource()

api.add_route('/leaders', leaders)