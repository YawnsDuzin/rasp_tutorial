#!/usr/bin/env python3
"""
HC-SR04 초음파 거리 센서 예제
실시간으로 거리를 측정합니다.

회로:
HC-SR04 VCC -- 5V (핀 2)
HC-SR04 TRIG -- GPIO23 (핀 16)
HC-SR04 ECHO -- [1kΩ] -- GPIO24 (핀 18)
                [2kΩ] -- GND (전압 분배기)
HC-SR04 GND -- GND (핀 6)

⚠️ 주의: ECHO 핀은 5V를 출력하므로 전압 분배기 필요!
"""

from gpiozero import DistanceSensor
from time import sleep

# 거리 센서 (ECHO=24, TRIGGER=23)
sensor = DistanceSensor(echo=24, trigger=23)

print("초음파 거리 센서")
print("Ctrl+C로 종료\n")

try:
    while True:
        distance_cm = sensor.distance * 100
        print(f"거리: {distance_cm:.1f} cm")
        sleep(1)

except KeyboardInterrupt:
    print("\n종료")
