# 🏭 NEXUS IIoT — Sistem Pemantauan Produksi Pabrik Susu

NEXUS IIoT adalah platform *Industrial Monitoring* berbasis **Internet of Things (IoT)** yang dirancang untuk mengawasi parameter kritis pada lini produksi susu secara *real-time*. Sistem ini mengintegrasikan akuisisi data sensor melalui protokol MQTT, penyimpanan NoSQL MongoDB, dan antarmuka HMI (*Human Machine Interface*) yang futuristik.



## 🚀 Fitur Utama

- **Real-Time Monitoring Dashboard:** Visualisasi data sensor (Suhu, Tekanan, Level Tangki, pH, dan *Flow Rate*) dari 5 area produksi dengan pembaruan data setiap 3 detik.
- **Industrial Control Panel:** Dilengkapi dengan *Gauge* interaktif dan status aktuator virtual (Valve & Pompa) yang bekerja berdasarkan logika kondisi sensor.
- **Smart Alert System:**
  - **Floating Notification:** Notifikasi melayang otomatis saat parameter sensor berada di zona bahaya.
  - **Audio Alarm:** Pemicu sirine otomatis (`alarm_alert.mp3`) untuk memberikan peringatan auditif kepada operator.
  - **Alert Log:** Pencatatan riwayat peringatan (Warning/Danger) yang tersimpan secara lokal.
- **Data Reporting & Audit:** Fitur ekspor data produksi 24 jam terakhir langsung ke format CSV untuk kebutuhan dokumentasi dan analisis manufaktur.

## 🛠️ Tech Stack

| Komponen | Teknologi |
| --- | --- |
| **Frontend** | HTML5, CSS3 (Neon/Cyberpunk Theme), JavaScript (Vanilla), Chart.js |
| **Backend API** | Python 3, Flask, Flask-CORS |
| **Messaging Protocol** | MQTT (Paho-MQTT v2) |
| **Database** | MongoDB (NoSQL) |
| **Environment** | Python-Dotenv (Security Management) |



## 📂 Struktur Proyek

- **`iot-dashboard.html`**: Antarmuka web utama menggunakan desain *dark mode* futuristik.
- **`api_susu.py`**: Backend Flask yang bertugas menyediakan *endpoint* data JSON dan fungsi ekspor CSV.
- **`sub_susu.py`**: Layanan *subscriber* yang menerima data dari broker MQTT dan menyimpannya ke MongoDB.
- **`pub_susu.py`**: Simulator mesin produksi yang mempublikasikan data sensor secara acak (dengan logika anomali).
- **`alarm_alert.mp3`**: File audio sirine untuk sistem peringatan bahaya.
- **`.env`**: File konfigurasi rahasia (Password & IP) yang tidak dipublikasikan ke repositori.

## ⚙️ Cara Menjalankan Sistem

### 1. Instalasi Dependensi
Pastikan Anda memiliki Python 3 terpasang, lalu jalankan perintah berikut:
```bash
pip install flask flask-cors pymongo paho-mqtt python-dotenv
```

### 2. Konfigurasi Environment
Buat file `.env` di folder utama dan sesuaikan kredensial berikut:
```env
MONGO_HOST=IP_SERVER_ANDA
MONGO_PORT=948
MONGO_USER=USER_ANDA
MONGO_PASSWORD=PASSWORD_ANDA
DATABASE_NAME=kelompok1_pabrik_susu_enak_banget

MQTT_BROKER=IP_BROKER_ANDA
MQTT_PORT=34423
MQTT_USER=USER_MQTT
MQTT_PASS=PASSWORD_MQTT
```

### 3. Eksekusi Program
Jalankan skrip berikut pada terminal yang berbeda secara berurutan:
1. **Subscriber**: `python sub_susu.py` (Memulai mendengarkan data).
2. **API Server**: `python api_susu.py` (Menyalakan jembatan data ke web).
3. **Publisher**: `python pub_susu.py` (Mensimulasikan data sensor).
4. Buka `iot-dashboard.html` di browser Anda.

## 👥 Tim Pengembang
**Kelompok 1 - 1AEC-1 - 2026 — Politeknik Manufaktur Bandung**
*Project ini dikembangkan sebagai bagian dari pemenuhan tugas mata kuliah Basisdata NoSQL.*