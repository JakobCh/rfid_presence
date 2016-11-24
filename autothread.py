#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import config

#user = config.ftpuser
#passwd = config.ftppasswd
#serverip = config.ftpserverip

def threadprint(st):
	print("THREAD:" + st)

def autothread(checkbase, tagdb, inst=False):
	lastwritetime = time.time()
	while 1:
		checkbase.updateMaxTime() #kolla om någon har varit inne längre än en lektion
		
		if lastwritetime + config.ftpupdatetime < time.time() or inst: #om det har gått 10 minuter sen sista gången
			threadprint("Removing old exel files")
			os.system("rf -rf " + checkbase.savepath) #ta bort alla exel filer
			threadprint("Cleaning out old checkins")
			checkbase.cleanup() #ta bort gammla in/ut checkningar
			threadprint("Creating new exel files")
			checkbase.createexelfiles(tagdb) #skapa nya exel filer
			
			threadprint("Sending exel files to server..")
			#os.system('ncftpput -R -u "' + user + '" -p "' + passwd + '" ' + serverip + ' ' + config.ftpfolder + ' ' + checkbase.savepath)
			os.system('cp -r exel/ ' + config.ftpfolder)
			threadprint("DONE")
			lastwritetime = time.time() #sätt ny tid
			if inst:
				return
	time.sleep(10)
			

