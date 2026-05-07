@echo off
cd /d "d:\FILE ALL\FOLDER KULIAH\NoSQL Praktek\Python Industri\crud sensor"
echo Starting MQTT Publisher...
start "Publisher" python mqtt_publisher.py
echo Starting MQTT Subscriber...
python mqtt_subsciber.py
pause
