#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import pickle #library used to save variables to file
#import rfid #our rfid module
import RPi.GPIO as GPIO
import signal
import MFRC522
from tagdatabase import tagdatabase
from incheckdatabase import incheckdatabase
from LcdControler import LcdControler

databasefile = "databases/tagdatabase.pickle"  #[tagid,name,class]
databasefile2 = "databases/inoroutdatabase.pickle" #[name, time, in/out]

if not os.path.exists("databases/"):
	os.makedirs("databases/")

yesarray = ["y", "Y", "yes", "Yes"]
noarray = ["n", "N", "no", "No"]

def catchstop(a,b): #om processen stopas så körs den här först innan den stängs av
	print("Stop signal detected")
	GPIO.cleanup() #fixar till gpio portarna
	lcd.lcd_stop() #sickar signal till lcd displayen att cleara skärmen
	print("Saving..")
	checkbase.save()
	tagdb.save()
	print("Save done")
	print("Quiting")
	sys.exit()
	
	
	
def addTag():
	print("Put a tag on the reader")
	
	while True:
	
		(status,TagType) = MIFAREREADER.MFRC522_Request(MIFAREREADER.PICC_REQIDL) #is a tag there
		if status == MIFAREREADER.MI_OK:
			print("Found tag")
	
		(status,uid) = MIFAREREADER.MFRC522_Anticoll() #get uid
		#tagid = "2B53B49B"
		if status == MIFAREREADER.MI_OK:
			tagid = tagdb.uidToTagid(uid)
			user = tagdb.isInTagList(tagid)
			if user:
				print("Id: " + tagid + " is already in use by " + user)
				print("Do you want to chance it?")
				choise = raw_input()
				if choise in yesarray:
					print("Enter a new name for: " + tagid)
					newname = raw_input().title().decode("utf-8")
					print("Enter a class for: " + newname + " : " + tagid)
					cla = raw_input().upper()
					tagdb.addTag(tagid, newname, cla)
					print(newname + " added with id: " + tagid + " and class: " + cla)
					tagdb.save()
					return True
					
				elif choise in noarray:
					print("Okay then")
					return False
				else:
					print("That is not a valid answer")
					return False
			else:
				print("Enter a new name for: " + tagid)
				newname = raw_input().title()
				print("Enter a class for: " + newname + " : " + tagid)
				cla = raw_input().upper()
				tagdb.addTag(tagid, newname, cla)
				print(newname + " added with id: " + tagid + " and class: " + cla)
				tagdb.save()
				return True

def manualAddTag():
	print("Enter id:")
	tagid = raw_input()
	print("Enter name:")
	newname = raw_input().title()
	print("Enter class:")
	cla = raw_input().upper()

	tagdb.addTag(tagid, newname, cla)
	tagdb.save()
	return True
	
def removeTag():
	print("Put a tag on the reader")
	while True:
		(status,TagType) = MIFAREREADER.MFRC522_Request(MIFAREREADER.PICC_REQIDL)
		if status == MIFAREREADER.MI_OK:
			print("Found tag")
	
		(status,uid) = MIFAREREADER.MFRC522_Anticoll()
		if status == MIFAREREADER.MI_OK:
			tagid = tagdb.uidToTagid(uid)
			user = tagdb.isInTagList(tagid)
			tagdb.removeTag(tagid)
			print(user + ": " + tagid + ". removed from tags")
			tagdb.save()
			break
			
def manualRemoveTag():
	print("Enter id:")
	tagid = raw_input()
	tagdb.removeTag(tagid)
	user = tagdb.isInTagList(tagid)
	cla = tagdb.getClassById(tagid)
	print(tagid + " with name:" + user + " and class:" + cla)
	tagdb.save()
	
def ReadOnce():
	print("Waiting for tag...")
	while True:
		#rfid.waitTag() #wait for a tag
		(status,TagType) = MIFAREREADER.MFRC522_Request(MIFAREREADER.PICC_REQIDL)
		if status == MIFAREREADER.MI_OK:
			print("Found tag, Tag type: " + str(TagType))
		
		(status,uid) = MIFAREREADER.MFRC522_Anticoll()
		if status == MIFAREREADER.MI_OK:
			
			tagid = tagdb.uidToTagid(uid) #convert uid to tagid ()
			
			user = tagdb.isInTagList(tagid) #check if the Tag is in the Tag list, if so it returns the name
			if user:
				cla = tagdb.getClassById(tagid)
				print("User:" + user + " Class:" + cla)
			else:
				print("Unknown Tag: " + tagid)
				
			break

			
def help():
	print("Jakob Christofferssons Rfid närvaro program")
	print("Andvänding: Main.py [Augment]")
	print("	run	kör närvaro sekvensen")
	print("	add	länka en taggar till ett namn")
	print("	remove	ta bort en tagg från databasen")
	print("	menu	öppnar en menu för olika functioner")
	print("	dump	dumpar informationen lagrad i databasen till exel filer")
	print("	cleanup <Dagar>	tar bort alla incheckningar som är mer än 10 dagar gammla eller <Dagar> gammla")

signal.signal(signal.SIGINT, catchstop) #om vi blir sickade en SIGINT (Ctrl-C) så kör funktionen catchstop
signal.signal(signal.SIGTERM, catchstop) #om vi blir sickade en SIGTERM (pkill) så kör funktionen catchstop

MIFAREREADER = MFRC522.MFRC522()
checkbase = incheckdatabase(databasefile2)
tagdb = tagdatabase(databasefile)
lcd = LcdControler()
lcd.lcd_init()

if len(sys.argv) == 2:
	if sys.argv[1] == "add":
		addTag()
	elif sys.argv[1] == "remove":	
		removeTag()
	elif sys.argv[1] == "help":
		help()
	elif sys.argv[1] == "cleanup":
		if len(sys.argv) == 3:
			checkbase.cleanup(days=int(sys.argv[2]))
		else:
			checkbase.cleanup()
	elif sys.argv[1] == "dump":
		checkbase.createexelfiles(tagdb)
	elif sys.argv[1] == "menu":
		while True:
			#sys.clear()
			print("Menu:")
			print("1. Add a new tag")
			print("2. Manual add tag")
			print("3. Show Tag list")
			print("4. Remove tag")
			print("5. Manual remove tag")
			print("6. Read tag")
			print("7. Dump checkin data")
			print("8. nicedump checkin data")
			print("9. exel dump")
			print("10. lcd test")
			print("11. Show Class list")
			choise = int(raw_input())
			if choise == 1:
				addTag()
			elif choise == 2:
				manualAddTag()
			elif choise == 3:
				tagdb.printTagList()
			elif choise == 4:
				removeTag()
			elif choise == 5:
				try:
					manualRemoveTag()
				except:
					1+1
			elif choise == 6:
				ReadOnce()
			elif choise == 7:
				checkbase.dump()
			elif choise == 8:
				checkbase.nicedump()
			elif choise == 9:
				#nims = checkbase.getNames()
				#print checkbase.nametoexellist(nims[0])
				checkbase.createexelfiles(tagdb)
			elif choise == 10:
				lcd.lcd_string("1234567890123456", lcd.LCD_LINE_1)
				lcd.lcd_string("1234567890123456", lcd.LCD_LINE_2)
				print("The lcd sould now display:")
				print("1234567890123456")
				print("1234567890123456")
				print("")
			elif choise == 11:
				print tagdb.getAllClasses()
				
	elif sys.argv[1] == "run":
		checkbase = incheckdatabase(databasefile2)
		print("Jakobs rfid reader TM")
		print("Waiting for tag..")
		while True:
			(status,TagType) = MIFAREREADER.MFRC522_Request(MIFAREREADER.PICC_REQIDL) #måste köras innan MIFAREREADER.MFRC522_Anticoll(), ansluter till tagen??
			if status == MIFAREREADER.MI_OK:
				print("Found tag")
			
			(status,uid) = MIFAREREADER.MFRC522_Anticoll() #försök läsa uid från tagen,
			if status == MIFAREREADER.MI_OK: #om det gick bra
				
				tagid = tagdb.uidToTagid(uid) #kenvertera uid listan till en string
				
				user = tagdb.isInTagList(tagid) #check if the Tag is in the Tag list, if so it returns the name
				if user:
					shortuser = user[0:16]
					inorout, cooldown = checkbase.addData(user, time.time())
					if cooldown:
						print("User:" + user + " Tag:" + tagid + " is on cooldown")
						lcd.lcd_string(shortuser, lcd.LCD_LINE_1)
						lcd.lcd_string("FEL", lcd.LCD_LINE_2)
						time.sleep(2)
						lcd.lcd_string("du har nyss", lcd.LCD_LINE_1)
						lcd.lcd_string("kommit in/ut", lcd.LCD_LINE_2)
					else:
						if inorout:
							print("User:" + user + " Tag:" + tagid + " State: IN")
							lcd.lcd_string(shortuser, lcd.LCD_LINE_1)
							#lcd.lcd_string("State: IN", lcd.LCD_LINE_2)
							lcd.lcd_string("Du kommer IN", lcd.LCD_LINE_2)
						else:
							print("User:" + user + " Tag:" + tagid + " State: OUT")
							lcd.lcd_string(shortuser, lcd.LCD_LINE_1)
							#lcd.lcd_string("State: OUT", lcd.LCD_LINE_2)
							lcd.lcd_string("Du gar UT", lcd.LCD_LINE_2)
					
				else:
					print("Unknown tag: " + tagid)
					lcd.lcd_string("Okänd tag", lcd.LCD_LINE_1)
					lcd.lcd_string(":(", lcd.LCD_LINE_2)
					
				time.sleep(2)
					
			checkbase.updateMaxTime() #kolla om någon har varit inne längre än en lektion
			lcd.lcd_string("Valkommen!", lcd.LCD_LINE_1) #skriv till första raden på lcdn
			lcd.lcd_string("Lagg pa din tag", lcd.LCD_LINE_2) #skriv till andra raden på lcdn
	else:
		help()
else:
	help()
	
catchstop(1,2)
	