#!/usr/bin/env python3
"""
버튼으로 LED 제어 예제
버튼을 누르면 LED가 켜지고, 떼면 꺼집니다.

회로:
- LED: GPIO17 (핀 11) -- [330Ω] -- LED -- GND
- 버튼: 3.3V (핀 1) -- 버튼 -- GPIO27 (핀 13) -- [10kΩ] -- GND
"""

from gpiozero import LED, Button
from signal import pause

# 부품 설정
led = LED(17)
button = Button(27)

print("버튼으로 LED 제어")
print("버튼을 눌러보세요! (Ctrl+C로 종료)")

# 버튼을 누르면 LED 켜기
button.when_pressed = led.on

# 버튼을 떼면 LED 끄기
button.when_released = led.off

try:
    # 프로그램이 계속 실행되도록
    pause()

except KeyboardInterrupt:
    print("\n종료")

finally:
    led.close()
