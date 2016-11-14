#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

user = "root"
passwd = "nas4free"
serverip = "10.1.1.15"

def autothread(checkbase, tagdb):
	lastwritetime = time.time()
	while 1:
		checkbase.updateMaxTime() #kolla om någon har varit inne längre än en lektion
		
		if lastwritetime + 60*10 < time.time(): #om det har gått 10 minuter sen sista gången
			os.system("rf -rf " + checkbase.savepath) #ta bort alla exel filer
			checkbase.cleanup() #ta bort gammla in/ut checkningar
			checkbase.createexelfiles(tagdb) #skapa nya exel filer
			
			os.system('ncftpput -R -u "' + user + '" -p "' + passwd + '" ' + serverip + ' /Närvaro/ ' + checkbase.savepath)
			
			lastwritetime = time.time() #sätt ny tid
			
			

