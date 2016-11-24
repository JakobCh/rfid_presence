#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import time
import math
import os
from exelbook import exelbook
import config

class incheckdatabase():
	def __init__(self):
		self.filepath = config.databasefolder + config.incheckdatabasefile #s�t databas filen till den i configen
		self.data = [] #h�r lagrar vi al skit
		#datan ser ut s�h�r =
		#[namn, tid, in eller ut checkning]
		self.savepath = config.exelsavepath
		
		
		self.load() #k�r load function f�r att ladda in databas filen in i self.data
		self.lessontime = 60*80 #80 min lektionstid
		self.maxCheckinTime = self.lessontime + 60*10 #lektions tid + 10
		self.checkincooldown = 60 #1 minut
		
	def cleanup(self, days=10):
		currenttime = time.time()
		for i in self.data:
			if i[1] < currenttime - 60*60*24*days: #days dagar gammla (default 10)
				self.data.remove(i)
				
		
		
	def save(self):
		with open(self.filepath, "wb") as f: #�ppna database filen 
			pickle.dump(self.data, f, 2) #ta self.data och spara i filen
			
	def load(self):
		try: #f�rs�k
			with open(self.filepath) as f: #�ppna database filen
				self.data = pickle.load(f) #ladda in datan i filen till self.data
		except: #om n�got gick fel
			self.data = [] #s� blir self.data tom
			
	def addData(self, name, tim): #namn och vilken tid
		inorout = True #False �r ute och true �r inne, sate den till true ifall det var f�rsta g�ngen man n�gonsin har checkat in
		namechecktemp = self.getLastCheckinFromName(name) #f� sista incheckningen fr�n det namnet
		if not namechecktemp == []: #om vi hitta en inceckning fr�n namenet
			inorout = namechecktemp[2] #s�t inorout till den sista incheckninges v�rde
			inorout = not inorout #invertera det s� om man har g�tt in s� g�r man nu ut
			lastcheckintime = namechecktemp[1]
		else:
			lastcheckintime = 0
		
		if time.time() - lastcheckintime > self.checkincooldown: #om det har g�tt self.checkincooldown sedan sista incheckningen s�
			self.data.append([name, tim, inorout]) #l�g in en ny checkning
			self.save() #spara databasen
			return inorout, False #vi sickar tilbacka om det var en incheckning eller en utcheckning och att tagen inte var p� cooldown
		else: #om det inte har g�tt self.checkincooldown sedan sista inceckningen
			return inorout, True #sicka tillbacka true eftersom det �r p� cooldown
		
	def updateMaxTime(self): #andv�nds f�r att kolla om n�gon �r incheckad f�r l�nge
		for name in self.getNames(): #loopa igenom alla namn vi har sparade
			namecheckin = self.getLastCheckinFromName(name) #f� den sista in/ut checkningen fr�n det namnet
			if namecheckin[2] == True: #om det var en incheckning
				if time.time() - namecheckin[1] > self.maxCheckinTime: #om inceckningen h�nde f�r mer �n self.maxCheckinTime sen s�
					self.addData(namecheckin[0], namecheckin[1]) #l�ger vi in en ny utcheckning samma tid som dom kom in
					print(name + " hit max checkin time")
					
		
	def getLastCheckinFromName(self, nam):
		chek = [] #s�tter chek till en tom lista ifall man inte hittar n�gon med det namnet
		for i in self.data: #g� igenom databasen
			if i[0] == nam: #om namnet matchar s�
				chek = i #s�tter vi chek till den listan i databasen
						 #p� detta set s� f�r vi den sista listan med det namnet kvar efter
				
		return chek #sicka tillbaka den sista listan med namnet eller bara [] om vi inte hitta n�gon 
		
	def namedatasort(self, name):
		namelist = [] #listan som vi kommer ha all data som har med name och g�ra
		for i in self.data: #g� igenom v�r data
			if i[0] == name: #om datan har r�tt namn som vi letar efter
				namelist.append(i) #l�g till datan i v�r lista
		return namelist #sicka tillbacka listan
		
	def getNames(self):
		namelist = []
		for i in self.data:
			if not i[0] in namelist:
				namelist.append(i[0])
		return namelist
		
	def timeformat(self, ti): #tid till time,minut,sekund + datum
		return time.strftime("%R:%S %e/%m/%Y", time.localtime(ti))
		
	def timeformat2(self, ti): #tid till time,minut,sekund
		return time.strftime("%R:%S", time.localtime(ti))
		
	def timeformat3(self, ti): #tid till datum
		return time.strftime("%e/%m/%Y", time.localtime(ti))
		
	def timeformat4(self, ti): #vecka
		return time.strftime("%W", time.localtime(ti))
		
	def timeformat5(self, ti): #�r
		return time.strftime("%Y", time.localtime(ti))
		
	def dump(self):
		for i in self.data: #g� igenom datan
			#print(i)
			print(i[0], self.timeformat(i[1]), i[2]) #skriv ut namn, tid och on dom gick in eller ut
			
	def nicedump(self):
		timestart = 0
		timeend = 0
		names = self.getNames()
		oldname = ""
		#print(names)
		for name in names:
			for i in self.data:
				if i[0] == name:
					if i[2] == True:
						timestart = i[1]
					elif i[2] == False:
						timeend = i[1]
						print(i[0] + ": " + self.timeformat2(timestart) + " - " + self.timeformat(timeend))
						timestart = 0
						timeend = 0
						oldname = name
			
			if timeend == 0 and not timestart == 0:
				print(name + ": " + self.timeformat2(timestart) + " - " + (" " * len(self.timeformat2(timestart))) + " " + self.timeformat3(timestart))
			
	def nametoexellist(self, name):
		#listlist = []
		#currentlistindex = 0
		starttime = 0
		gonetime = 0
		templist = []
		for i in self.data:
			if i[0] == name:
				#print(i[0])
				if i[2]:
					inut = "In"
					starttime = i[1]
					templist.append([inut, self.timeformat3(i[1]), self.timeformat2(i[1])])
				else:
					inut = "Ut"
					if i[1] == starttime:
						gonetime = self.lessontime
					
					if gonetime == 0:
						templist.append([inut, self.timeformat3(i[1]), self.timeformat2(i[1]), self.timeformat2(i[1] - starttime - 60*60*1)]) #fick l�gga till minus en time?
					else:
						templist.append([inut, self.timeformat3(i[1]), self.timeformat2(i[1]), "", self.timeformat2(gonetime - 60*60*1)]) #h�r ocks�, annars blev det 1 timme f�r mycket
					
					gonetime = 0
					
		#mybook = exelbook()
		#mybook.setTitle(name)
		#mybook.advancedwrite(templist)
		#mybook.save()
		return templist	
		
	def createexelfiles(self, tagdb):
		names = self.getNames()
		currenttime = time.time()
		week = str(self.timeformat4(currenttime))
		year = str(self.timeformat5(currenttime))
		directory = self.savepath + year + '/' + config.exelweekname + ' ' + week + "/"
		if not os.path.exists(directory):
			os.makedirs(directory)
			
		for name in names:
			cla = tagdb.getClassByName(name)
			mybook = exelbook()
			mybook.setTitle(name.decode("utf-8"))
			print(directory + cla + "/" + name + ".xlsx")
			mybook.advancedwrite(self.nametoexellist(name))
			if not os.path.exists(directory + cla + "/"):
				os.makedirs(directory + cla + "/")
			mybook.saveas(directory + cla + "/" + name + ".xlsx")
				
				
if __name__ == "__main__":
	testdb = incheckdatabase()
	testdb.nicedump()