#!/bin/bash

if pgrep "python" > /dev/null
then
	echo "Rfid_presence is already running."
else
	echo "Rfid_presence is starting up."
	nohup python -u Main.py run &
fi
