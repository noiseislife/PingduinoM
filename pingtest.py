#!/usr/bin/python

"""
    PingduinoM - Visual ping using Arduino and BlinkM

    Copyright (c) Pat Arneson - http://noiseislife.tumblr.com
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.

    Also find me on twitter @noise_is_life	
"""

import os,string,sys,ping,socket,time,serial

def toBlinkM (ser, command):
	ser.write(command.decode("hex"))

def setBlinkMToPlaySimpleScript (ser, address, color1, color2, color3, color4, duration, fadespeed):
	# example: write line 0 of script 0 on BlinkM 1
	# 	01	Start code
	#	01	BlinkM address
	#	08	bytes to send
	#	00	bytes to receive
	#	57	command: write line
	#	00	script number
	#	00	line number
	#	20	duration
	#	63	fade
	#	20	R
	#	20	G
	#	00	B

	print ("> Playing Simple Script on "+address)

	toBlinkM(ser, "01"+address+"0800570000"+duration+"63"+color1)
	time.sleep (.2)
	toBlinkM(ser, "01"+address+"0800570001"+duration+"63"+color2)
	time.sleep (.2)
	toBlinkM(ser, "01"+address+"0800570002"+duration+"63"+color3)
	time.sleep (.2)
	toBlinkM(ser, "01"+address+"0800570003"+duration+"63"+color4)
	time.sleep (.2)
	# last line: play script 0 1 time
	toBlinkM(ser, "01"+address+"0800570004"+"00"+"70"+"000100")
	time.sleep (.2)

	# set script id 0 to a len. of 5, 1 repeats
	toBlinkM(ser, "01"+address+"04004C000501")
	time.sleep (.2)

	# set fade speed
	toBlinkM(ser, "01"+address+"020066"+fadespeed)
	time.sleep (.2)

	# play script id 0
	toBlinkM(ser, "01"+address+"040070008000")
	time.sleep (.2)

try:
    ser = serial.Serial('COM3',19200, timeout=1)
    counter = 0

    print "> Waiting for Arduino."

    while 1:
            serialline = ser.readline()
            if (serialline):
                    print serialline.strip()
            if ('ready' in serialline):
                    break

    print "> Arduino ready."

    # tell #1 to stop animating
    toBlinkM(ser, "010901006f")

    # init min/max
    isFirst = True
    pingMin = None
    # Collect a few pings to increase the chances of a good initial min ping
    for i in range(1,10):
        if isFirst:
            while (pingMin == None):
                pingMin = ping.do_one('www.google.com', timeout=2)
            isFirst = False
        else:
            while (pingMin == None):
                pingMin = min(pingMin,ping.do_one('www.google.com', timeout=2))
    # pingMax is arbitrarily set to 10x the minimum, it seems to work for my environ.
    pingMax = pingMin * 10
    print 'Calculated Min: %s Max: %s' % (pingMin,pingMax) 
    while (True):
        delays = []
        for i in range(1,10):
            delay = ping.do_one('www.google.com', timeout=2)
            if (delay == None):
                delay = 2
            delays.append(delay)
            if delay <> None:
                # Reset min and max if new min is found, resets in case of a bad start
                pingMin = min(pingMin,delay)
                pingMax = pingMin * 10
        delayAvg =  sum(delays) / len(delays)

        delayMS = int(delayAvg * 1000)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if delayAvg > pingMax:
            print '%s Blink Red: %s' % (timeStr,delayMS)
            setBlinkMToPlaySimpleScript(ser,"09","FF0000","FF0000","000000","000000","05","10")
        elif delayAvg > pingMax / 2:
            print '%s Red: %s' % (timeStr,delayMS)
            toBlinkM(ser, "010901006f")         # stop animating
            toBlinkM(ser, "0109040063FF0000")   # fade to red
        elif delayAvg > (pingMin * 3):
            print '%s Yellow: %s' % (timeStr,delayMS)
            toBlinkM(ser, "010901006f")         # stop animating
            toBlinkM(ser, "0109040063FF3300")   # fade to yellow
        else:
            toBlinkM(ser, "010901006f")         # stop animating
            toBlinkM(ser, "010904006300FF00")   # fade to green

        time.sleep(2)
except socket.error, e:
    print "Ping Error:", e
except KeyboardInterrupt:
    print "Exit."
    # This makes the BlinkM go dark on exit.  There is undoubtedly a better way.
    setBlinkMToPlaySimpleScript(ser,"09","000000","000000","000000","000000","05","10")
    toBlinkM(ser, "010901006f")         # stop animating
    toBlinkM(ser, "0109040063000000")   # fade to black
