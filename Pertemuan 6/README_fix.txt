FIXES FOR "ERROR TERUS":

PROBLEM: test.mosquitto.org MQTT broker timeout (high latency ~250ms from ping, connect timeout too short).

SOLUTION 1 - Install & run local MQTT broker:
1. pip install mosquitto (or download from eclipse.org/mosquitto)
2. Run broker: mosquitto -v
3. Then run: python mqtt_publisher.py & python mqtt_subsciber.py

SOLUTION 2 - Increase timeout in files (updated mqtt_subsciber.py already):
Edit mqtt_publisher.py line ~15:
client.connect("test.mosquitto.org", 1883, 120)  # 120s timeout

SOLUTION 3 - Use public broker with better latency:
Edit both files:
BROKER = "broker.hivemq.com"
or
BROKER = "mqtt.eclipseprojects.io"

DB is fine (103 docs in praktikum6.sensor).

Test: Kill test_sub.py terminals (Ctrl+C), run fix 1 or 2.
