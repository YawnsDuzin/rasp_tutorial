# 09. 센서 활용

다양한 센서를 라즈베리파이와 연결하여 환경 데이터를 수집하고 활용하는 방법을 배웁니다.

## 센서 종류

### 환경 센서
- 온습도 센서 (DHT11, DHT22)
- 기압 센서 (BMP280)
- 조도 센서 (LDR, BH1750)

### 거리/모션 센서
- 초음파 거리 센서 (HC-SR04)
- 적외선 거리 센서
- PIR 모션 센서

### 기타 센서
- 소리 센서
- 진동 센서
- 가스 센서

## DHT11/DHT22 온습도 센서

### DHT11 vs DHT22

| 특징 | DHT11 | DHT22 |
|------|-------|-------|
| **가격** | 저렴 ($2~3) | 약간 비쌈 ($5~10) |
| **온도 범위** | 0~50°C | -40~80°C |
| **온도 정확도** | ±2°C | ±0.5°C |
| **습도 범위** | 20~80% | 0~100% |
| **습도 정확도** | ±5% | ±2~5% |
| **샘플링 주기** | 1Hz (1초당 1회) | 0.5Hz (2초당 1회) |

### 회로 구성

```
DHT11/DHT22        Raspberry Pi
VCC    ----------  3.3V (핀 1)
DATA   ----------  GPIO4 (핀 7)
GND    ----------  GND (핀 6)
```

### 라이브러리 설치

```bash
sudo apt update
sudo apt install python3-pip
sudo pip3 install adafruit-circuitpython-dht
sudo apt install libgpiod2
```

### Python 코드

```python
import time
import board
import adafruit_dht

# DHT22 센서 (GPIO4 사용)
dht_device = adafruit_dht.DHT22(board.D4)
# DHT11 사용 시: adafruit_dht.DHT11(board.D4)

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
    print("프로그램 종료")
    dht_device.exit()
```

**파일 저장**: `dht_sensor.py`

**실행**:
```bash
python3 dht_sensor.py
```

## HC-SR04 초음파 거리 센서

### 작동 원리

초음파를 발사하고 반사되어 돌아오는 시간을 측정하여 거리 계산

### 회로 구성

```
HC-SR04            Raspberry Pi
VCC    ----------  5V (핀 2)
TRIG   ----------  GPIO23 (핀 16)
ECHO   ----------  [1kΩ 저항] -- GPIO24 (핀 18)
                   [2kΩ 저항] -- GND
GND    ----------  GND (핀 6)
```

⚠️ **주의**: ECHO 핀은 5V를 출력하므로 전압 분배기로 3.3V로 낮춰야 함!

### Python 코드

```python
import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # 트리거 신호 보내기
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 마이크로초
    GPIO.output(TRIG, False)

    # 에코 신호 대기
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # 거리 계산
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # 음속 = 34300 cm/s
    distance = round(distance, 2)

    return distance

try:
    while True:
        dist = measure_distance()
        print(f"거리: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("측정 종료")
    GPIO.cleanup()
```

### gpiozero 사용 (더 간단)

```python
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=24, trigger=23)

try:
    while True:
        print(f"거리: {sensor.distance * 100:.1f} cm")
        sleep(1)

except KeyboardInterrupt:
    print("종료")
```

## PIR 모션 센서

### 특징

- 적외선으로 사람/동물의 움직임 감지
- 보안 시스템, 자동 조명에 사용

### 회로 구성

```
PIR 센서           Raspberry Pi
VCC    ----------  5V (핀 2)
OUT    ----------  GPIO17 (핀 11)
GND    ----------  GND (핀 6)
```

### Python 코드

```python
from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(17)

def motion_detected():
    print("모션 감지!")

def no_motion():
    print("모션 없음")

pir.when_motion = motion_detected
pir.when_no_motion = no_motion

print("PIR 센서 모니터링 시작...")
pause()
```

### LED와 연동

```python
from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(17)
led = LED(27)

# 모션 감지 시 LED 자동 켜기
pir.when_motion = led.on
pir.when_no_motion = led.off

print("모션 감지 조명 시작!")
pause()
```

## BMP280 기압 센서 (I2C)

### I2C 활성화

```bash
sudo raspi-config
# Interface Options → I2C → Enable
```

### 회로 구성

```
BMP280             Raspberry Pi
VCC    ----------  3.3V (핀 1)
GND    ----------  GND (핀 6)
SCL    ----------  GPIO3/SCL (핀 5)
SDA    ----------  GPIO2/SDA (핀 3)
```

### 라이브러리 설치

```bash
sudo apt install python3-smbus i2c-tools
sudo pip3 install adafruit-circuitpython-bmp280
```

### I2C 주소 확인

```bash
i2cdetect -y 1
```

### Python 코드

```python
import board
import adafruit_bmp280

# I2C 버스 초기화
i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# 해수면 기압 설정 (지역별 다름)
bmp280.sea_level_pressure = 1013.25

try:
    while True:
        print(f"온도: {bmp280.temperature:.1f}°C")
        print(f"기압: {bmp280.pressure:.2f} hPa")
        print(f"고도: {bmp280.altitude:.2f} m")
        print("-" * 30)

        import time
        time.sleep(2)

except KeyboardInterrupt:
    print("종료")
```

## LDR (조도 센서)

### 회로 구성 (MCP3008 ADC 사용)

라즈베리파이는 아날로그 입력이 없으므로 ADC(Analog to Digital Converter)가 필요합니다.

```
LDR → MCP3008 → Raspberry Pi (SPI)
```

### Python 코드

```python
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        light_level = read_adc(0)
        print(f"조도: {light_level}")
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
```

## 실전 프로젝트: 환경 모니터링 시스템

### 온습도 + 기압 통합

```python
import time
import board
import adafruit_dht
import adafruit_bmp280

# 센서 초기화
dht = adafruit_dht.DHT22(board.D4)
i2c = board.I2C()
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

def get_sensor_data():
    try:
        temp_dht = dht.temperature
        humidity = dht.humidity
        temp_bmp = bmp.temperature
        pressure = bmp.pressure

        return {
            "temperature": round((temp_dht + temp_bmp) / 2, 1),
            "humidity": round(humidity, 1),
            "pressure": round(pressure, 2)
        }
    except RuntimeError:
        return None

try:
    while True:
        data = get_sensor_data()

        if data:
            print(f"""
            === 환경 데이터 ===
            온도: {data['temperature']}°C
            습도: {data['humidity']}%
            기압: {data['pressure']} hPa
            시각: {time.strftime('%Y-%m-%d %H:%M:%S')}
            ==================
            """)

        time.sleep(10)

except KeyboardInterrupt:
    print("모니터링 종료")
    dht.exit()
```

## 데이터 로깅 및 시각화

### CSV 파일로 저장

```python
import csv
import time
from datetime import datetime

def log_to_csv(data):
    with open('sensor_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([
            timestamp,
            data['temperature'],
            data['humidity'],
            data['pressure']
        ])

# 사용
data = get_sensor_data()
if data:
    log_to_csv(data)
```

### 그래프 그리기 (matplotlib)

```bash
sudo apt install python3-matplotlib
```

```python
import matplotlib.pyplot as plt
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('sensor_log.csv',
                 names=['timestamp', 'temp', 'humidity', 'pressure'])

# 그래프 그리기
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(df['temp'])
plt.title('온도')
plt.ylabel('°C')

plt.subplot(3, 1, 2)
plt.plot(df['humidity'])
plt.title('습도')
plt.ylabel('%')

plt.subplot(3, 1, 3)
plt.plot(df['pressure'])
plt.title('기압')
plt.ylabel('hPa')

plt.tight_layout()
plt.savefig('sensor_graph.png')
plt.show()
```

## 문제 해결

### DHT 센서 읽기 오류

- 2초 이상 간격으로 읽기
- 전원 및 배선 확인
- 풀업 저항 추가 (4.7kΩ~10kΩ, VCC-DATA 사이)

### I2C 장치가 인식 안 됨

```bash
# I2C 활성화 확인
sudo raspi-config

# I2C 도구로 스캔
i2cdetect -y 1

# 권한 문제 시
sudo usermod -a -G i2c $USER
```

### 초음파 센서 값이 불안정

- 센서를 평평한 표면에 향하게
- 측정 간격 늘리기
- 여러 번 측정하여 평균값 사용

## 다음 단계

센서 사용법을 배웠습니다! 이제 Python 프로그래밍으로 더 복잡한 프로젝트를 만들어봅시다.

➡️ [다음: Python 프로그래밍](../05-programming/python-programming.md)

## 참고 자료

- [Adafruit 센서 라이브러리](https://github.com/adafruit/Adafruit_CircuitPython_DHT)
- [GPIO Zero 센서 가이드](https://gpiozero.readthedocs.io/en/stable/recipes.html)
- [센서 구매처](https://www.adafruit.com/)
