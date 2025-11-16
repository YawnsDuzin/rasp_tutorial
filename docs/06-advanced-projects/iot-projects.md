# 13. IoT 프로젝트

라즈베리파이를 사용하여 사물인터넷(IoT) 프로젝트를 만드는 방법을 배웁니다.

## IoT란?

**IoT (Internet of Things, 사물인터넷)**는 인터넷에 연결된 장치들이 데이터를 수집하고 공유하는 기술입니다.

### IoT의 구성 요소

1. **센서/액추에이터**: 데이터 수집 및 제어
2. **통신**: Wi-Fi, Bluetooth, MQTT 등
3. **클라우드**: 데이터 저장 및 분석
4. **애플리케이션**: 사용자 인터페이스

## MQTT 프로토콜

### MQTT란?

**MQTT (Message Queuing Telemetry Transport)**는 IoT 장치 간 통신에 최적화된 경량 프로토콜입니다.

### MQTT 구조

- **Broker**: 메시지 중개 서버
- **Publisher**: 메시지를 발행하는 클라이언트
- **Subscriber**: 메시지를 구독하는 클라이언트
- **Topic**: 메시지 주제/채널

### Mosquitto MQTT Broker 설치

```bash
# Mosquitto 설치
sudo apt update
sudo apt install mosquitto mosquitto-clients

# 서비스 시작
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# 상태 확인
sudo systemctl status mosquitto
```

### Python MQTT 클라이언트

```bash
pip install paho-mqtt
```

## MQTT Publisher (센서 데이터 전송)

### 온도 데이터 발행

```python
# mqtt_publisher.py
import paho.mqtt.client as mqtt
import time
import json
import board
import adafruit_dht

# MQTT 설정
MQTT_BROKER = "localhost"  # 또는 브로커 IP
MQTT_PORT = 1883
MQTT_TOPIC = "home/livingroom/temperature"

# DHT 센서
dht_device = adafruit_dht.DHT22(board.D4)

# MQTT 클라이언트 생성
client = mqtt.Client("RaspberryPi_Sensor")

# 브로커 연결
client.connect(MQTT_BROKER, MQTT_PORT)

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
                print(f"Published: {data}")

        except RuntimeError as error:
            print(f"Sensor error: {error.args[0]}")

        time.sleep(10)  # 10초마다 전송

except KeyboardInterrupt:
    print("Stopping...")
    client.disconnect()
    dht_device.exit()
```

## MQTT Subscriber (데이터 수신)

### 데이터 구독 및 처리

```python
# mqtt_subscriber.py
import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "home/livingroom/temperature"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 연결 성공 시 토픽 구독
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}")
    print(f"Message: {msg.payload.decode()}")

    # JSON 파싱
    try:
        data = json.loads(msg.payload.decode())
        print(f"온도: {data['temperature']}°C")
        print(f"습도: {data['humidity']}%")
        print(f"시각: {data['timestamp']}")
        print("-" * 40)
    except json.JSONDecodeError:
        print("Invalid JSON")

# MQTT 클라이언트 생성
client = mqtt.Client("RaspberryPi_Receiver")

# 콜백 함수 설정
client.on_connect = on_connect
client.on_message = on_message

# 브로커 연결
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 메시지 수신 대기 (무한 루프)
client.loop_forever()
```

## 클라우드 IoT 플랫폼

### ThingSpeak 연동

**ThingSpeak**는 무료 IoT 데이터 플랫폼입니다.

#### 1. ThingSpeak 계정 생성

- [https://thingspeak.com/](https://thingspeak.com/)에서 가입
- 새 채널 생성
- API Key 복사

#### 2. 데이터 전송

```bash
pip install requests
```

```python
# thingspeak_upload.py
import requests
import time
import board
import adafruit_dht

# ThingSpeak 설정
API_KEY = "YOUR_WRITE_API_KEY"
URL = "https://api.thingspeak.com/update"

# 센서 초기화
dht_device = adafruit_dht.DHT22(board.D4)

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None:
                # ThingSpeak로 전송
                params = {
                    'api_key': API_KEY,
                    'field1': temperature,
                    'field2': humidity
                }

                response = requests.get(URL, params=params)

                if response.status_code == 200:
                    print(f"Uploaded: Temp={temperature}°C, Humidity={humidity}%")
                else:
                    print(f"Upload failed: {response.status_code}")

        except RuntimeError as error:
            print(f"Sensor error: {error.args[0]}")

        time.sleep(15)  # ThingSpeak 무료 계정은 15초 간격

except KeyboardInterrupt:
    print("Stopped")
    dht_device.exit()
```

### Blynk 앱 연동

**Blynk**는 스마트폰 앱으로 IoT 장치를 제어할 수 있는 플랫폼입니다.

#### 설치

```bash
pip install blynk-library-python
```

#### 코드 예제

```python
import BlynkLib
import time
from gpiozero import LED

# Blynk 인증 토큰 (Blynk 앱에서 생성)
BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

# Blynk 연결
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# LED
led = LED(17)

# 가상 핀 V1로 LED 제어
@blynk.on("V1")
def v1_write_handler(value):
    if int(value[0]) == 1:
        led.on()
        print("LED ON")
    else:
        led.off()
        print("LED OFF")

# 가상 핀 V2로 온도 전송 (예제)
def send_temperature():
    temperature = 25.5  # 실제 센서 값 사용
    blynk.virtual_write(2, temperature)

# 메인 루프
try:
    while True:
        blynk.run()
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")
    led.close()
```

## 스마트홈 자동화

### Home Assistant 연동

**Home Assistant**는 오픈소스 스마트홈 플랫폼입니다.

#### Home Assistant 설치

```bash
# Docker로 설치 (권장)
sudo apt install docker.io
sudo docker run -d \
    --name homeassistant \
    --restart=unless-stopped \
    -v /home/pi/homeassistant:/config \
    -e TZ=Asia/Seoul \
    --network=host \
    ghcr.io/home-assistant/home-assistant:stable
```

접속: `http://raspberrypi.local:8123`

#### MQTT 센서 설정

**configuration.yaml**:
```yaml
mqtt:
  broker: localhost
  port: 1883

sensor:
  - platform: mqtt
    name: "거실 온도"
    state_topic: "home/livingroom/temperature"
    unit_of_measurement: "°C"
    value_template: "{{ value_json.temperature }}"

  - platform: mqtt
    name: "거실 습도"
    state_topic: "home/livingroom/temperature"
    unit_of_measurement: "%"
    value_template: "{{ value_json.humidity }}"
```

## 실전 프로젝트: 스마트 온도 제어 시스템

### 기능
- 온도 센서로 실내 온도 측정
- 설정 온도보다 높으면 팬 켜기
- 데이터를 MQTT로 전송
- 웹 대시보드로 모니터링

```python
# smart_temperature_control.py
import paho.mqtt.client as mqtt
import time
import json
import board
import adafruit_dht
from gpiozero import OutputDevice

# 설정
TEMP_THRESHOLD = 28  # 온도 임계값
MQTT_BROKER = "localhost"
MQTT_TOPIC = "home/climate/control"

# 하드웨어 초기화
dht_device = adafruit_dht.DHT22(board.D4)
fan = OutputDevice(17)  # 릴레이 또는 트랜지스터로 팬 제어

# MQTT 클라이언트
client = mqtt.Client("ClimateControl")
client.connect(MQTT_BROKER)

def control_fan(temperature):
    if temperature > TEMP_THRESHOLD:
        fan.on()
        return "ON"
    else:
        fan.off()
        return "OFF"

try:
    print("스마트 온도 제어 시작...")

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None:
                # 팬 제어
                fan_status = control_fan(temperature)

                # 데이터 생성
                data = {
                    "temperature": round(temperature, 1),
                    "humidity": round(humidity, 1),
                    "fan_status": fan_status,
                    "threshold": TEMP_THRESHOLD,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                # MQTT 발행
                client.publish(MQTT_TOPIC, json.dumps(data))

                print(f"온도: {temperature}°C | 팬: {fan_status}")

        except RuntimeError as error:
            print(f"센서 오류: {error.args[0]}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n시스템 종료")
    fan.off()
    client.disconnect()
    dht_device.exit()
```

## 보안 고려사항

### MQTT 보안

#### 1. 사용자 인증 설정

```bash
# 비밀번호 파일 생성
sudo mosquitto_passwd -c /etc/mosquitto/passwd username

# 설정 파일 수정
sudo nano /etc/mosquitto/mosquitto.conf
```

**추가**:
```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

#### 2. TLS/SSL 암호화

```bash
# 인증서 생성 (자체 서명)
cd /etc/mosquitto/certs
sudo openssl req -new -x509 -days 365 -extensions v3_ca \
    -keyout ca.key -out ca.crt

# mosquitto.conf에 추가
listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

#### 3. Python에서 인증 사용

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()

# 사용자 인증
client.username_pw_set("username", "password")

# TLS 설정
client.tls_set("/etc/mosquitto/certs/ca.crt")

client.connect("broker_address", 8883)
```

## 다음 단계

IoT 기초를 배웠습니다! 다른 고급 프로젝트들도 살펴봅시다.

➡️ [다음: 카메라 프로젝트](camera-projects.md)

## 참고 자료

- [Mosquitto 문서](https://mosquitto.org/documentation/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [ThingSpeak](https://thingspeak.com/)
- [Home Assistant](https://www.home-assistant.io/)
- [Blynk](https://blynk.io/)
