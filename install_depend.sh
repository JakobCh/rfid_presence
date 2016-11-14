sudo apt-get update
sudo apt-get upgrade	
sudo apt-get install python-dev git openpyxl

cd ~
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
sudo python setup.py install
cd ~
rm -rf SPI-Py/

cd ~
git clone https://github.com/mxgxw/MFRC522-python.git
cp MFRC522-python/MFRC522.py rfid_presence/
rm -rf MFRC522-python/

echo "python -u ~/rfid_presence/Main.py run" >> ~/.bashrc