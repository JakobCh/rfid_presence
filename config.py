
databasefolder = "databases/"
tagdatabasefile = "tagdatabase.pickle"  #stores name-class-tagid records     [tagid,name,class]
incheckdatabasefile = "inoroutdatabase.pickle" #stores all checkin/outs         [name, time, in/out]

lessontime = 60*80 #80 min
maxCheckinTime = lessontime + 60*10 #lesson time plus 10 min
checkincooldown = 60 #1 min, cooldown between checkins

#EXEL
exelsavepath = "exel/"
exelweekname = "Vecka"
#exelweekname = "Week"
exelwords = ["In/Ut", "Datum", "Stämpel", "Lektionstid", "Frånvaro", "Anm"]

#FTP
#ftpuser = "narvaro"
#ftppasswd = "rfidnas"
#ftpserverip = "10.1.1.15"
ftpfolder = '/mnt/Larare/Närvaro/'
ftpupdatetime = 60*10 #i sekunder (10 min default)




#LCD
lcdbacklight = True

#I dont recommend chancing anything after this point
lcdi2caddr = 0x27
lcdsmbus = 1 # Rev 2 Pi uses 1
			 # Rev 1 Pi uses 0
#More LCD options can be found in the LcdControler file


