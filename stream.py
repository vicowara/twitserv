#-*- coding:utf-8 -*-

import datetime
import tweepy
import subprocess
import threading
from systemd import journal
import config
from config import api
from plugins import commands,commands_with_args

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if config.screen_name == status.in_reply_to_screen_name:
			# TODO: 正規表現で書きなおす
			# 「@vicowara command arg1 arg2 //comment」から「command arg1 arg2 //comment」を抜き出す
			reply = status.text.lstrip("@" + config.screen_name).lstrip()
			# 「//comment」を削除する
			if reply.find("//") > 0:
				reply = reply[:reply.index("//")].rstrip()

			# コマンドに引数があるか確認
			reply_args = None
			if len(reply.split()) > 1:
				reply_args = reply.split()[1:]
				reply = reply.split()[0]

			# その他、結果を返信するためのidやリプライ元など
			reply_id = status.id
			reply_name = status.user.screen_name

			# 引数がない場合
			if reply in commands and reply_args is None:
				#print(" ".join(["[", str(datetime.datetime.now()), "]: received", reply, "message from", reply_name]))
				journal.send(" ".join(["received", reply, "message from", reply_name]))
				th = threading.Thread(target=(lambda: api.update_status("".join(["@", reply_name, "\n", commands[reply]()])[:140], in_reply_to_status_id = reply_id)))
				th.start()

			# 引数がある場合
			if reply in commands_with_args and reply_args is not None:
				#print(" ".join(["[", str(datetime.datetime.now()), "]: received", reply] + reply_args + ["message from", reply_name]))
				journal.send(" ".join(["received", reply] + reply_args + ["message from", reply_name]))
				th = threading.Thread(target=(lambda *args: api.update_status("".join(["@", reply_name, "\n", commands_with_args[reply](args)])[:140], in_reply_to_status_id = reply_id)), args=reply_args)
				th.start()
		return True

	def on_error(self, status):
		#print("error:{}".format(status))
		journal.send("error:{}".format(status))
		return True

	def on_timeout(self):
		#print("timeout")
		journal.send("timeout")
		return True
