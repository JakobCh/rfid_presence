#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import config 

class tagdatabase():
	def __init__(self):
		self.tags = []
		self.databasefile = config.databasefolder + config.tagdatabasefile
		self.load()
		
		
	def load(self):
		try: #försök
			with open(self.databasefile) as f: #öppna databas filen
				self.tags = pickle.load(f) #andvänd pickle för att ladda in variablerna vi har sparat till tags
		except: #om det inte gick
			self.tags = []
			
	def save(self):
		with open(self.databasefile, "wb") as f:
			pickle.dump(self.tags, f, 2)
			
	def isInTagList(self, key):
		for i in self.tags:
			if i[0] == key:
				return i[1]
		return False
		
	def getClassByName(self, name):
		for i in self.tags:
			if i[1] == name:
				return i[2]
		return False
		
	def getClassById(self, tagid):
		for i in self.tags:
			if i[0] == tagid:
				return i[2]
		return False
		
	def getAllClasses(self):
		donelist = []
		for i in self.tags:
			if not i[2] in donelist:
				donelist.append(i[2])
		return donelist
		
	def uidToTagid(self, uid):
		return str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
		
	def addTag(self, tagid, name, cla): #tagid name class
		user = self.isInTagList(tagid)
		if user:
			self.tags.remove([tagid, name, cla])	
			self.tags.append([tagid, name, cla])
		else:
			self.tags.append([tagid, name, cla])
			
	def removeTag(self, tagid):
		try:
			name = self.isInTagList(tagid)
			cla = self.getClassByName(name)
			self.tags.remove([tagid, name, cla])
		except:
			print("Tried to remove non existing tagid")
		
	def printTagList(self):
		for i in self.tags:
			#print(i[0]) #will print all the Tag ids
			#print(i[1]) #will print all the names
			print('"' + i[0] + '":"' + i[1] + '":"' + i[2] + '"')
			
	def fixCap(self):
		for i in self.tags:
			tempstring = i[1]
			tempstring = tempstring.decode('utf-8').title()
			i[1] = tempstring