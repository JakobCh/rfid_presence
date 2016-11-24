sudo apt-get update
#sudo apt-get upgrade	
sudo apt-get install python-dev git ncftp nohup sshfs
pip install openpyxl

cd ~
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
sudo python setup.py install
cd ~
sudo rm -rf SPI-Py/

cd ~
git clone https://github.com/mxgxw/MFRC522-python.git
cp MFRC522-python/MFRC522.py rfid_presence/
sudo rm -rf MFRC522-python/

echo "cd ~/rfid_presence/" >> ~/.bashrc
echo 'if pgrep "python" > /dev/null' >> ~/.bashrc
echo 'then' >> ~/.bashrc
echo 'echo "rfid_presence already running"' >> ~/.bashrc 
echo 'else' >> ~/.bashrc
echo "nohup python -u Main.py run &" >> ~/.bashrc
echo "fi" >> ~/.bashrc
echo "cd ~" >> ~/.bashrc