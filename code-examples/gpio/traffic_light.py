#!/usr/bin/env python3
"""
신호등 시뮬레이션
빨강 -> 노랑 -> 초록 순서로 LED가 켜집니다.

회로:
- 빨강 LED: GPIO17 -- [330Ω] -- LED -- GND
- 노랑 LED: GPIO27 -- [330Ω] -- LED -- GND
- 초록 LED: GPIO22 -- [330Ω] -- LED -- GND
"""

from gpiozero import LED
from time import sleep

# LED 설정
red = LED(17)
yellow = LED(27)
green = LED(22)

print("신호등 시뮬레이션 시작 (Ctrl+C로 종료)")

try:
    while True:
        # 빨간불
        print("🔴 빨간불")
        red.on()
        sleep(3)
        red.off()

        # 노란불
        print("🟡 노란불")
        yellow.on()
        sleep(1)
        yellow.off()

        # 초록불
        print("🟢 초록불")
        green.on()
        sleep(3)
        green.off()

except KeyboardInterrupt:
    print("\n신호등 종료")

finally:
    red.close()
    yellow.close()
    green.close()
