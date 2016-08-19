#-*- coding:utf-8 -*-

import tweepy
import subprocess
import datetime
import pyowm
from config import api, forbidden_names, owm_token, default_location

speedtest_lastupdate = None
speedtest_cache = None


# speedtest --simpleの結果を返す
# 10分以内に実行されていた場合エラーとしてエラーメッセージを返す
def speedtest():
	global speedtest_lastupdate
	# 初回起動でなく、かつ10分以内に実行されていればエラーメッセージを返して終了
	if (speedtest_lastupdate is not None) and (datetime.datetime.now() - speedtest_lastupdate < datetime.timedelta(minutes=10)):
		return "It has not yet been 10 minutes since last speedtest. Abort."
	# 最終実行時間の更新
	speedtest_lastupdate = datetime.datetime.now()
	try:
		result = subprocess.check_output(['speedtest-cli','--simple'], universal_newlines=True)
	except subprocess.CalledProcessError as e:
		result = "speedtest failed({})".format(e.returncode)
	return "".join(["Speedtest Result:\n",result])


# iwconfig wlan0の結果からRSSIとS/N比を返す
# shellに投げているので下手なことをするとセキュリティ的に危ない
def rssi():
	try:
		result = subprocess.check_output('LANG=C sh -c "iwconfig wlan0|grep Quality"', universal_newlines=True, shell=True).lstrip()
	except subprocess.CalledProcessError as e:
		result = "iwconfig failed({})".format(e.returncode)
	return result


# vcgencmd measure_tempから温度を出す
def temperature():
	try:
		result = subprocess.check_output(['vcgencmd', 'measure_temp'], universal_newlines=True).lstrip()
	except subprocess.CalledProcessError as e:
		result = "iwconfig failed({})".format(e.returncode)
	return result


# 名前を変える
def name_change(args):
	name = " ".join(args)
	for n in forbidden_names:
		if n in name:
			return ""
	name = name[:20]
	try:
		api.update_profile(name=name)
		result = name + "に変更しました"
	except tweepy.error.TweepError as e:
		result = e.reason
	return result

# 応用情報試験日までの残り日数
def ouyou():
	d = datetime.datetime.strptime("2016-10-16 09:00:00","%Y-%m-%d %H:%M:%S")-datetime.datetime.now()
	if d.total_seconds() > 0:
		return "平成28年度秋期情報処理技術者試験まで残り " + str(d)
	else:
		return "平成28年度秋期情報処理技術者試験は 2016-10-16 09:00:00 に開催されました"

# 今日の天気
def weather(*args):
	try:
		location = str(args[0])
	except:
		location = default_location
	owm = pyowm.OWM(owm_token)
	fc = owm.three_hours_forecast(location)

	if fc == None:
		return "その都市は存在しません"

	weathers = fc.get_forecast().get_weathers()

	result = []
	now = datetime.datetime.today()
	tommorow = now + datetime.timedelta(hours=24)

	for i in weathers:
		t = datetime.datetime.fromtimestamp(i.get_reference_time())
		status = i.get_detailed_status()
		
		if now < t and t < tommorow:
			result.append("".join([str(t.hour), "時: ", status, "\n"]))

	return "".join(result)

# no argument commands
# 辞書形式で{"実行コマンド名":関数名}を連名していく
# commands_with_argsと競合する関数は原則として入れないほうが良い

commands = {"speedtest":speedtest, "rssi":rssi, "応用":ouyou, "ouyou":ouyou, "応用情報":ouyou, "temperature":temperature, "温度":temperature, "weather":weather, "天気":weather}

# with arguments commands

commands_with_args = {"name_change":name_change, "名前変更":name_change, "change_name":name_change, "update_name":name_change, "name_update":name_change, "weather":weather, "天気":weather}
