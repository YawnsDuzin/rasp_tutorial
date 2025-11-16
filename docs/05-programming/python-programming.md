# 10. Python 프로그래밍

라즈베리파이에서 Python을 사용하여 다양한 프로젝트를 만드는 방법을 배웁니다.

## Python 기초

### Python 버전 확인

```bash
python3 --version
```

Raspberry Pi OS에는 Python 3가 기본으로 설치되어 있습니다.

### 첫 Python 프로그램

```python
# hello.py
print("Hello, Raspberry Pi!")
```

**실행**:
```bash
python3 hello.py
```

## 가상 환경 (Virtual Environment)

### 가상 환경이란?

프로젝트별로 독립적인 Python 패키지 환경을 만듭니다.

### 가상 환경 생성 및 사용

```bash
# 가상 환경 생성
python3 -m venv myproject_env

# 활성화
source myproject_env/bin/activate

# 비활성화
deactivate
```

### 패키지 설치

```bash
# 가상 환경 내에서
pip install requests
pip install flask
pip install numpy

# requirements.txt로 관리
pip freeze > requirements.txt
pip install -r requirements.txt
```

## GPIO 프로그래밍 심화

### 멀티 스레딩

여러 작업을 동시에 수행:

```python
import threading
from gpiozero import LED, Button
from signal import pause
import time

led1 = LED(17)
led2 = LED(27)
button = Button(22)

def blink_led1():
    while True:
        led1.toggle()
        time.sleep(1)

def blink_led2():
    while True:
        led2.toggle()
        time.sleep(0.5)

# 스레드 생성
thread1 = threading.Thread(target=blink_led1, daemon=True)
thread2 = threading.Thread(target=blink_led2, daemon=True)

# 스레드 시작
thread1.start()
thread2.start()

# 버튼으로 종료
button.when_pressed = lambda: exit()

print("LED 깜빡임 시작 (버튼 누르면 종료)")
pause()
```

### 타이머와 스케줄링

```python
import schedule
import time
from gpiozero import LED

led = LED(17)

def job():
    print("작업 실행!")
    led.on()
    time.sleep(1)
    led.off()

# 10초마다 실행
schedule.every(10).seconds.do(job)

# 매일 특정 시간에 실행
schedule.every().day.at("09:00").do(job)

# 매주 월요일에 실행
schedule.every().monday.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

**설치**:
```bash
pip install schedule
```

## 파일 처리

### 텍스트 파일 읽기/쓰기

```python
# 쓰기
with open('data.txt', 'w') as f:
    f.write("라즈베리파이 데이터\n")
    f.write("온도: 25.5°C\n")

# 읽기
with open('data.txt', 'r') as f:
    content = f.read()
    print(content)

# 줄 단위로 읽기
with open('data.txt', 'r') as f:
    for line in f:
        print(line.strip())
```

### JSON 파일 처리

```python
import json
from datetime import datetime

# 데이터 구조
sensor_data = {
    "timestamp": datetime.now().isoformat(),
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25
}

# JSON 파일로 저장
with open('sensor_data.json', 'w') as f:
    json.dump(sensor_data, f, indent=2)

# JSON 파일 읽기
with open('sensor_data.json', 'r') as f:
    data = json.load(f)
    print(f"온도: {data['temperature']}°C")
```

### CSV 파일 처리

```python
import csv
from datetime import datetime

# CSV 쓰기
with open('log.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.now(),
        25.5,  # 온도
        60.2,  # 습도
        1013.25  # 기압
    ])

# CSV 읽기
with open('log.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

## 데이터베이스 (SQLite)

### SQLite 기초

```python
import sqlite3
from datetime import datetime

# 데이터베이스 연결
conn = sqlite3.connect('sensors.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL,
    pressure REAL
)
''')

# 데이터 삽입
cursor.execute('''
INSERT INTO sensor_readings (timestamp, temperature, humidity, pressure)
VALUES (?, ?, ?, ?)
''', (datetime.now().isoformat(), 25.5, 60.2, 1013.25))

conn.commit()

# 데이터 조회
cursor.execute('SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10')
rows = cursor.fetchall()

for row in rows:
    print(f"시간: {row[1]}, 온도: {row[2]}°C, 습도: {row[3]}%")

conn.close()
```

## 웹 스크래핑

### requests와 BeautifulSoup

```bash
pip install requests beautifulsoup4
```

```python
import requests
from bs4 import BeautifulSoup

# 웹페이지 가져오기
url = "https://example.com"
response = requests.get(url)

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 요소 찾기
title = soup.find('title')
print(f"제목: {title.text}")

# 모든 링크 가져오기
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
```

## API 활용

### 날씨 API 예제

```python
import requests
import json

# OpenWeatherMap API (무료 API 키 필요)
API_KEY = "your_api_key_here"
CITY = "Seoul"

url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    print(f"도시: {CITY}")
    print(f"온도: {temp}°C")
    print(f"습도: {humidity}%")
    print(f"날씨: {description}")
else:
    print("날씨 정보를 가져올 수 없습니다.")
```

## 이메일 전송

### SMTP로 이메일 보내기

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver@example.com"
    password = "your_app_password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
        print("이메일 전송 성공!")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

# 사용 예
send_email(
    "라즈베리파이 알림",
    "온도가 30°C를 넘었습니다!"
)
```

## 실전 프로젝트: 스마트 온도 모니터

### 기능
- 온습도 센서로 데이터 수집
- 데이터베이스에 저장
- 온도가 임계값 초과 시 이메일 알림
- 웹 API로 현재 날씨와 비교

```python
import time
import sqlite3
from datetime import datetime
import board
import adafruit_dht
import requests

# 설정
TEMP_THRESHOLD = 30  # 온도 임계값
CHECK_INTERVAL = 60  # 60초마다 체크

# 센서 초기화
dht_device = adafruit_dht.DHT22(board.D4)

# 데이터베이스 초기화
conn = sqlite3.connect('temperature_monitor.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL
)
''')
conn.commit()

def save_reading(temp, humidity):
    cursor.execute(
        'INSERT INTO readings (timestamp, temperature, humidity) VALUES (?, ?, ?)',
        (datetime.now().isoformat(), temp, humidity)
    )
    conn.commit()

def get_outdoor_temp():
    """외부 날씨 API에서 온도 가져오기 (예시)"""
    # 실제로는 API 키가 필요합니다
    return None

try:
    print("온도 모니터링 시작...")

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                print(f"  실내 온도: {temperature:.1f}°C")
                print(f"  실내 습도: {humidity:.1f}%")

                # 데이터베이스에 저장
                save_reading(temperature, humidity)

                # 임계값 체크
                if temperature > TEMP_THRESHOLD:
                    print(f"⚠️  경고: 온도가 {TEMP_THRESHOLD}°C를 초과했습니다!")
                    # send_email() 함수 호출 가능

                print("-" * 40)

        except RuntimeError as error:
            print(f"센서 읽기 오류: {error.args[0]}")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n모니터링 종료")
    dht_device.exit()
    conn.close()
```

## 유용한 Python 패키지

### 데이터 처리
```bash
pip install numpy pandas matplotlib
```

### 웹 개발
```bash
pip install flask django
```

### IoT 및 통신
```bash
pip install paho-mqtt requests
```

### 컴퓨터 비전
```bash
pip install opencv-python picamera2
```

## 다음 단계

Python 프로그래밍 기초를 배웠습니다! 이제 웹 서버를 구축해봅시다.

➡️ [다음: 웹 서버 구축](web-server.md)

## 참고 자료

- [Python 공식 문서](https://docs.python.org/3/)
- [Real Python 튜토리얼](https://realpython.com/)
- [라즈베리파이 Python 가이드](https://www.raspberrypi.com/documentation/computers/os.html#python)
