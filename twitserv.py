#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import tweepy

from stream import MyStreamListener
from config import auth


def main():
        stream = tweepy.Stream(auth, MyStreamListener(), secure=True)
        while True:
                try:
                        stream.userstream()
                except Exception as e:
                        print(e)

if __name__ == "__main__":
	main()
