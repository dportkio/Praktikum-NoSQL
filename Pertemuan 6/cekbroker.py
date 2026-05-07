import paho.mqtt.client as mqtt
import time

# Fungsi ini otomatis dipanggil pas dapet respon dari broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Mantap wok! Berhasil konek ke broker MQTT.")
    else:
        print(f"Gagal konek nih, kode error-nya: {rc}")

# Setup client
client = mqtt.Client()
client.on_connect = on_connect

print("Lagi nyoba nyambungin ke test.mosquitto.org...")

try:
    # Coba konek ke broker di port 1883
    client.connect("test.mosquitto.org", 1883, 60)
    
    # Jalanin background loop sebentar buat nerima respon
    client.loop_start()
    time.sleep(3) # Tunggu 3 detik
    client.loop_stop()
except Exception as e:
    print(f"Brokernya lagi down atau koneksi lu bermasalah: {e}")