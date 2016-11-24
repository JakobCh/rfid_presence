#!/bin/sh

if pgrep "python" > /dev/null
then
	echo "Rfid_presence is already running."
else
	echo "Rfid_presence is starting up."
	nohup python Main.py run &
fi
