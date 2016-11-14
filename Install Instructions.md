#raspberrypi 1 type B

setup raspbian
	sudo raspi-config
	1. Expand Filesystem
	3. Boot Options
		Console
	5. Internationalisation Options 
		Chance Keyboard Layout
		Chance Locale
		Chance Timezone
	2. Chance User Password #ändra lösen för admin kontot
	9. Advanced Options
		A2 Hostname #Om du vill
		A4 SSH JA #Andvändbart och andvänds för att sicka över excel fillerna
		A5 SPI JA #Andvänds för rfid läsaren
		A6 I2C JA #Andvänds för lcd-skärmen
	

Install python-dev and git
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python-dev git
	
Install openpyxl #excel python library
	sudo pip install openpyxl
	
Install nohup #might be installed by default?
	sudo apt-get install nohup

Install SPI-Py
	cd ~
	git clone https://github.com/lthiery/SPI-Py.git
	cd SPI-Py/
	sudo python setup.py install
	cd ~
	rm -rf SPI-Py/
	
	
Install rfid_presence
	git clone https://github.com/JakobCh/rfid_presence
	
Get the MFRC522 library
	git clone https://github.com/mxgxw/MFRC522-python.git
	cp MFRC522-python/MFRC522.py rfid_presence/
	rm -rf MFRC522-python/
	
Add the script to autorun:
	echo "python -u ~/rfid_presence/Main.py run" >> ~/.bashrc
	



