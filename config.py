#-*- coding:utf-8 -*-

import tweepy

__CONSUMER_KEY = ""
__CONSUMER_SECRET = ""
__ACCESS_TOKEN = ""
__ACCESS_SECRET = ""

auth = tweepy.OAuthHandler(__CONSUMER_KEY, __CONSUMER_SECRET)
auth.set_access_token(__ACCESS_TOKEN, __ACCESS_SECRET)

api = tweepy.API(auth)

screen_name = ""
forbidden_names = []

owm_token = ""
default_location = ""
