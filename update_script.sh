cd ~
echo "Moving old.."
cp -r rfid_presence rfid_presence_old
rm -rf rfid_presence
echo "Getting new.."
git clone https://github.com/JakobCh/rfid_presence.git

JCDIR="rfid_presence"

if [ -d "$JCDIR" ]; then
	echo "Copying over databases.."
	cp -r rfid_presence_old/databases/ rfid_presence/
	cp -r rfid_presence_old/exel/ rfid_presence/
	cp rfid_presence_old/MFRC522.py rfid_presence/
	echo "Removing old.."
	rm -rf rfid_presence_old
else
	echo "couldn't not fetch from github"

fi

echo "Done!"