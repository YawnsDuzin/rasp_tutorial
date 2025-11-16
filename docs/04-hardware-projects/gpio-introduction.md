# 08. GPIO 입문

라즈베리파이의 GPIO(General Purpose Input/Output) 핀을 사용하여 하드웨어를 제어하는 방법을 배웁니다.

## GPIO란?

**GPIO (General Purpose Input/Output)**는 범용 입출력 핀으로, 다양한 전자 부품과 센서를 연결하여 제어할 수 있습니다.

### GPIO로 할 수 있는 것들

- LED 켜고 끄기
- 버튼 입력 읽기
- 센서 데이터 수집
- 모터 제어
- 디스플레이 출력
- 통신 (I2C, SPI, UART)

## GPIO 핀 배치

### Raspberry Pi 4/5 (40핀)

```
3V3  (1) (2)  5V
GPIO2  (3) (4)  5V
GPIO3  (5) (6)  GND
GPIO4  (7) (8)  GPIO14
GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND
GPIO22 (15) (16) GPIO23
3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND
GPIO9  (21) (22) GPIO25
GPIO11 (23) (24) GPIO8
GND (25) (26) GPIO7
GPIO0  (27) (28) GPIO1
GPIO5  (29) (30) GND
GPIO6  (31) (32) GPIO12
GPIO13 (33) (34) GND
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
GND (39) (40) GPIO21
```

### 핀 종류

1. **전원 핀**:
   - `5V` (핀 2, 4): 5볼트 전원
   - `3.3V` (핀 1, 17): 3.3볼트 전원
   - `GND` (핀 6, 9, 14, 20, 25, 30, 34, 39): 접지

2. **GPIO 핀** (GPIO0~GPIO27):
   - 디지털 입출력
   - 3.3V 로직 레벨
   - PWM, I2C, SPI, UART 기능 지원

### 핀 번호 체계

**BCM (Broadcom) 번호**:
- GPIO 번호 (GPIO2, GPIO3 등)
- 권장 방식

**BOARD (물리적) 번호**:
- 물리적 핀 위치 (1~40)

💡 **권장**: BCM 번호 사용

## 안전 수칙

⚠️ **중요**: GPIO 핀은 3.3V에서 작동합니다!

### 지켜야 할 규칙

1. **전압 주의**:
   - GPIO 핀에 5V 연결 금지 → 보드 손상
   - 3.3V만 사용

2. **전류 제한**:
   - 핀당 최대 16mA
   - 전체 최대 50mA
   - LED는 반드시 저항 사용

3. **단락(Short) 방지**:
   - GND와 전원 직접 연결 금지
   - 배선 확인 후 전원 인가

4. **정전기 방지**:
   - 보드 만지기 전 금속에 손 대기

## 첫 번째 프로젝트: LED 깜빡이기

### 필요한 부품

- LED × 1
- 저항 330Ω 또는 220Ω × 1
- 점퍼 와이어 (암수) × 2
- 브레드보드 (선택)

### 회로 구성

```
Raspberry Pi          LED
GPIO17 (핀 11) ----[저항 330Ω]----(+긴 다리)LED(-짧은 다리)---- GND (핀 6)
```

**연결 방법**:
1. GPIO17 (핀 11)에 저항의 한쪽 끝 연결
2. 저항의 다른 쪽 끝에 LED의 긴 다리(+, 양극) 연결
3. LED의 짧은 다리(-, 음극)를 GND에 연결

💡 **LED 극성**:
- 긴 다리: 양극 (+, 애노드)
- 짧은 다리: 음극 (-, 캐소드)

### Python 코드 (gpiozero 라이브러리)

```python
from gpiozero import LED
from time import sleep

# GPIO17 핀에 연결된 LED
led = LED(17)

# 5번 깜빡이기
for i in range(5):
    led.on()      # LED 켜기
    sleep(1)      # 1초 대기
    led.off()     # LED 끄기
    sleep(1)      # 1초 대기

print("완료!")
```

**파일 저장**: `blink.py`

**실행**:
```bash
python3 blink.py
```

### Python 코드 (RPi.GPIO 라이브러리)

```python
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정 (BCM 번호 사용)
GPIO.setmode(GPIO.BCM)

# 경고 메시지 비활성화
GPIO.setwarnings(False)

# GPIO17을 출력으로 설정
GPIO.setup(17, GPIO.OUT)

try:
    # 5번 깜빡이기
    for i in range(5):
        GPIO.output(17, GPIO.HIGH)  # LED 켜기
        time.sleep(1)
        GPIO.output(17, GPIO.LOW)   # LED 끄기
        time.sleep(1)
finally:
    # GPIO 정리
    GPIO.cleanup()

print("완료!")
```

## 두 번째 프로젝트: 버튼으로 LED 제어

### 필요한 부품

- LED × 1
- 푸시 버튼 × 1
- 저항 330Ω × 1
- 저항 10kΩ × 1 (풀다운용)
- 점퍼 와이어
- 브레드보드

### 회로 구성

```
[LED 회로]
GPIO17 (핀 11) ----[330Ω]----(+)LED(-)---- GND

[버튼 회로]
3.3V (핀 1) ---- 버튼 ---- GPIO27 (핀 13) ----[10kΩ]---- GND
```

### Python 코드

```python
from gpiozero import LED, Button
from signal import pause

# 부품 설정
led = LED(17)
button = Button(27)

# 버튼을 누르면 LED 켜기
button.when_pressed = led.on
# 버튼을 떼면 LED 끄기
button.when_released = led.off

print("버튼을 눌러보세요! (Ctrl+C로 종료)")
pause()  # 프로그램이 계속 실행되도록
```

**실행**:
```bash
python3 button_led.py
```

## GPIO 라이브러리 비교

### 1. gpiozero (권장)

**장점**:
- 초보자 친화적
- 간단한 문법
- 고수준 추상화

**설치**:
```bash
sudo apt install python3-gpiozero
```

**예제**:
```python
from gpiozero import LED
led = LED(17)
led.on()
led.off()
led.blink()  # 자동 깜빡임
```

### 2. RPi.GPIO

**장점**:
- 세밀한 제어
- 오랜 역사, 많은 예제
- 인터럽트 지원

**설치**:
```bash
sudo apt install python3-rpi.gpio
```

**예제**:
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.cleanup()
```

### 3. pigpio

**장점**:
- 하드웨어 PWM
- 정밀한 타이밍
- 네트워크 지원

**설치**:
```bash
sudo apt install pigpio python3-pigpio
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

## PWM (Pulse Width Modulation)

### PWM이란?

LED 밝기 조절, 모터 속도 제어 등에 사용되는 기술

### LED 밝기 조절 예제

```python
from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

# 서서히 밝아지기
for brightness in range(0, 100):
    led.value = brightness / 100
    sleep(0.02)

# 서서히 어두워지기
for brightness in range(100, 0, -1):
    led.value = brightness / 100
    sleep(0.02)

led.off()
```

### RGB LED 제어

```python
from gpiozero import RGBLED
from time import sleep

# RGB LED (각 색상별 GPIO 핀)
rgb = RGBLED(red=17, green=27, blue=22)

# 빨강
rgb.color = (1, 0, 0)
sleep(1)

# 초록
rgb.color = (0, 1, 0)
sleep(1)

# 파랑
rgb.color = (0, 0, 1)
sleep(1)

# 자주색 (빨강 + 파랑)
rgb.color = (1, 0, 1)
sleep(1)

# 흰색
rgb.color = (1, 1, 1)
sleep(1)

rgb.off()
```

## 유용한 도구

### 1. pinout 명령어

GPIO 핀 배치 확인:

```bash
pinout
```

또는 웹사이트: [https://pinout.xyz/](https://pinout.xyz/)

### 2. gpio 명령어 (WiringPi)

```bash
# 설치
sudo apt install wiringpi

# 핀 상태 확인
gpio readall

# GPIO 17 출력으로 설정
gpio mode 0 out

# GPIO 17 켜기
gpio write 0 1

# GPIO 17 끄기
gpio write 0 0
```

## 코드 예제 모음

### 예제 1: 신호등

```python
from gpiozero import LED
from time import sleep

red = LED(17)
yellow = LED(27)
green = LED(22)

while True:
    # 빨간불
    red.on()
    sleep(3)
    red.off()

    # 노란불
    yellow.on()
    sleep(1)
    yellow.off()

    # 초록불
    green.on()
    sleep(3)
    green.off()
```

### 예제 2: 버튼 카운터

```python
from gpiozero import Button
from signal import pause

button = Button(27)
counter = 0

def button_pressed():
    global counter
    counter += 1
    print(f"버튼 클릭 횟수: {counter}")

button.when_pressed = button_pressed

print("버튼을 눌러보세요!")
pause()
```

### 예제 3: 나이트 라이더

```python
from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(17, 27, 22, 5, 6, 13, 19, 26)

def knight_rider():
    # 왼쪽에서 오른쪽
    for led in leds:
        led.on()
        sleep(0.1)
        led.off()

    # 오른쪽에서 왼쪽
    for led in reversed(leds):
        led.on()
        sleep(0.1)
        led.off()

try:
    while True:
        knight_rider()
except KeyboardInterrupt:
    leds.off()
```

## 문제 해결

### LED가 켜지지 않음

1. **회로 확인**:
   - 배선이 올바른지 확인
   - LED 극성 확인 (긴 다리가 +)
   - 저항 연결 확인

2. **핀 번호 확인**:
   - BCM vs BOARD 번호 혼동
   - `pinout` 명령어로 확인

3. **권한 문제**:
   - `sudo python3 script.py` 실행
   - 또는 사용자를 gpio 그룹에 추가:
     ```bash
     sudo usermod -a -G gpio $USER
     # 로그아웃 후 다시 로그인
     ```

### 프로그램 종료 시 에러

항상 `GPIO.cleanup()` 또는 적절한 종료 처리:

```python
try:
    # 메인 코드
    pass
except KeyboardInterrupt:
    print("종료 중...")
finally:
    GPIO.cleanup()
```

## 다음 단계

GPIO 기초를 배웠습니다! 이제 다양한 센서를 사용해봅시다.

➡️ [다음: 센서 활용](sensors.md)

## 참고 자료

- [GPIO Zero 문서](https://gpiozero.readthedocs.io/)
- [RPi.GPIO 문서](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [핀아웃 다이어그램](https://pinout.xyz/)
- [라즈베리파이 GPIO 가이드](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header)
