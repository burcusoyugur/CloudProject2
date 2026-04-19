import json
import paho.mqtt.client as mqtt
import ssl
import time
import random


AWS_ENDPOINT = "a19b4l5agbr45b-ats.iot.eu-central-1.amazonaws.com" 
IOT_TOPIC = "binance/btc"

CA_PATH = "rootCA.pem"
CERT_PATH = "certificate.pem.crt"
KEY_PATH = "private.pem.key"

#AWS MQTT BAĞLANTISI 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("AWS Bulutuna başarıyla bağlandı!")
    else:
        print(f"Bağlantı hatası: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.tls_set(CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, tls_version=ssl.PROTOCOL_TLSv1_2)

print("AWS'ye bağlanılıyor...")
client.connect(AWS_ENDPOINT, 8883, 60)
client.loop_start()

#VERİ SİMÜLASYONU (Binance yerine)
print("Veri akışı başlatılıyor (Simülasyon)...")
try:
    base_price = 64000.0
    while True:
        # Gerçekçi bir fiyat dalgalanması oluşturuyoruz
        price_change = random.uniform(-10, 10)
        base_price += price_change
        
        payload = {
            "symbol": "BTCUSDT",
            "price": round(base_price, 2),
            "timestamp": int(time.time() * 1000)
        }
        
        print(f"Buluta Gönderiliyor: {payload['price']}")
        client.publish(IOT_TOPIC, json.dumps(payload), qos=1)
        time.sleep(2) # 2 saniyede bir gönder
except KeyboardInterrupt:
    print("Durduruldu.")
    client.disconnect()
