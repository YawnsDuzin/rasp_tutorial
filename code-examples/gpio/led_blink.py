#!/usr/bin/env python3
"""
LED 깜빡이기 예제
GPIO17 핀에 연결된 LED를 5번 깜빡입니다.

회로:
GPIO17 (핀 11) -- [330Ω 저항] -- LED(+긴다리) -- LED(-짧은다리) -- GND (핀 6)
"""

from gpiozero import LED
from time import sleep

# GPIO17 핀에 연결된 LED
led = LED(17)

print("LED 깜빡이기 시작...")

try:
    # 5번 깜빡이기
    for i in range(5):
        print(f"깜빡임 {i+1}/5")
        led.on()      # LED 켜기
        sleep(1)      # 1초 대기
        led.off()     # LED 끄기
        sleep(1)      # 1초 대기

    print("완료!")

except KeyboardInterrupt:
    print("\n사용자에 의해 중단됨")

finally:
    led.close()
