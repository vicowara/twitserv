#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys

import twitserv

from config import pidfile

def createDaemon():
	pid = os.fork()

	if pid > 0:
		# parent
		with open(pidfile, 'w') as f:
			f.write(str(pid) + "\n")

		sys.exit()
	elif pid == 0:
		# child
		twitserv.main()

if __name__ == '__main__':
	createDaemon()
