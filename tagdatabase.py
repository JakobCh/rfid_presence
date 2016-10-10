#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle

class tagdatabase():
	def __init__(self, file):
		self.tags = []
		self.databasefile = file
		self.load()
		
		
	def load(self):
		try: #f�rs�k
			with open(self.databasefile) as f: #�ppna databas filen
				self.tags = pickle.load(f) #andv�nd pickle f�r att ladda in variablerna vi har sparat till tags
		except: #om det inte gick
			self.tags = []
			
	def save(self):
		with open(self.databasefile, "w") as f:
			pickle.dump(self.tags, f)
			
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
		if not tagid.isalpha() and name.isalpha():
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