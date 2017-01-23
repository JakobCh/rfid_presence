
databasefolder = "databases/"
tagdatabasefile = "tagdatabase.pickle"  #stores name-class-tagid records     [tagid,name,class]
incheckdatabasefile = "inoroutdatabase.pickle" #stores all checkin/outs         [name, time, in/out]

lessontime = 60*80*2 + 60*20 #160 min + 20 min
maxCheckinTime = lessontime + 60*10 #lesson time plus 10 min
checkincooldown = 60 #1 min, cooldown between checkins

#EXEL
exelsavepath = "exel/"
exelweekname = "Vecka"
#exelweekname = "Week"
exelwords = ["In/Ut", "Datum", "Stämpel", "Lektionstid", "Frånvaro", "Anm"]

#FTP
ftpuser = "narvaro"
ftppasswd = "narvaro"

ftpserverip = "10.1.1.15"
ftpserverfolder = '/mnt/da1-backup/Närvaro' #folder on the server
ftpmountpoint = '/mnt/Närvaro' #were we mount it
ftpfolder = '/mnt/Närvaro/' #were we write our files to
ftpupdatetime = 60*10 #i sekunder (10 min default)




#LCD
lcdbacklight = True

#I dont recommend chancing anything after this point
lcdi2caddr = 0x27
lcdsmbus = 1 # Rev 2 Pi uses 1
			 # Rev 1 Pi uses 0
#More LCD options can be found in the LcdControler file


