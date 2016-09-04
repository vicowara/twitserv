#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import tweepy

from stream import MyStreamListener
from config import auth

if __name__=="__main__":
        stream = tweepy.Stream(auth, MyStreamListener(), secure=True)
        while True:
                try:
                        stream.userstream()
                except Exception as e:
                        print(e)
