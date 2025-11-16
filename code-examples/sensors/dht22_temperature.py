#!/usr/bin/env python3
"""
DHT22 온습도 센서 예제
실시간으로 온도와 습도를 측정합니다.

회로:
DHT22 VCC -- 3.3V (핀 1)
DHT22 DATA -- GPIO4 (핀 7)
DHT22 GND -- GND (핀 6)

필요 라이브러리:
sudo apt install python3-pip
sudo pip3 install adafruit-circuitpython-dht
sudo apt install libgpiod2
"""

import time
import board
import adafruit_dht

# DHT22 센서 (GPIO4 사용)
dht_device = adafruit_dht.DHT22(board.D4)

print("DHT22 온습도 센서 시작...")
print("Ctrl+C로 종료\n")

try:
    while True:
        try:
            # 온도와 습도 읽기
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            print(f"온도: {temperature:.1f}°C")
            print(f"습도: {humidity:.1f}%")
            print("-" * 30)

        except RuntimeError as error:
            # 센서 읽기 오류 (일시적)
            print(f"읽기 오류: {error.args[0]}")
            time.sleep(2.0)
            continue

        except Exception as error:
            dht_device.exit()
            raise error

        time.sleep(2.0)  # 2초 대기

except KeyboardInterrupt:
    print("\n프로그램 종료")
    dht_device.exit()
