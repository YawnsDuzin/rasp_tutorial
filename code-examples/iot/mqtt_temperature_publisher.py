#!/usr/bin/env python3
"""
MQTT 온도 데이터 Publisher
DHT22 센서의 온습도 데이터를 MQTT로 발행합니다.

설치:
sudo apt install mosquitto mosquitto-clients
pip install paho-mqtt
sudo pip3 install adafruit-circuitpython-dht
sudo apt install libgpiod2

실행:
python3 mqtt_temperature_publisher.py
"""

import paho.mqtt.client as mqtt
import time
import json
import board
import adafruit_dht

# MQTT 설정
MQTT_BROKER = "localhost"  # 또는 브로커 IP 주소
MQTT_PORT = 1883
MQTT_TOPIC = "home/livingroom/temperature"

# DHT22 센서
dht_device = adafruit_dht.DHT22(board.D4)

# MQTT 클라이언트 생성
client = mqtt.Client("RaspberryPi_TempSensor")

print(f"MQTT 브로커에 연결 중: {MQTT_BROKER}")
client.connect(MQTT_BROKER, MQTT_PORT)

print("온도 데이터 발행 시작...")
print("Ctrl+C로 종료\n")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                # JSON 데이터 생성
                data = {
                    "temperature": round(temperature, 1),
                    "humidity": round(humidity, 1),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                # MQTT 발행
                client.publish(MQTT_TOPIC, json.dumps(data))

                print(f"Published: 온도={data['temperature']}°C, 습도={data['humidity']}%")

        except RuntimeError as error:
            print(f"센서 읽기 오류: {error.args[0]}")

        time.sleep(10)  # 10초마다 전송

except KeyboardInterrupt:
    print("\n종료")
    client.disconnect()
    dht_device.exit()
