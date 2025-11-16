# 14. 카메라 프로젝트

라즈베리파이 카메라 모듈을 사용하여 사진, 비디오, 스트리밍 프로젝트를 만드는 방법을 배웁니다.

## 카메라 모듈

### 종류
- **Camera Module 3**: 최신, 12MP
- **Camera Module 2**: 8MP
- **HQ Camera**: 12.3MP, 렌즈 교환 가능
- **NoIR Camera**: 적외선, 야간 촬영

### 연결

CSI(Camera Serial Interface) 포트에 연결:
1. 라즈베리파이 전원 끄기
2. CSI 커넥터 열기
3. 케이블 삽입 (금속 접점이 HDMI 쪽)
4. 커넥터 닫기

### 카메라 활성화

```bash
sudo raspi-config
# Interface Options → Camera → Enable
```

## picamera2 라이브러리

### 설치 (Raspberry Pi OS Bullseye 이상)

```bash
sudo apt update
sudo apt install -y python3-picamera2
```

### 기본 사진 촬영

```python
# photo.py
from picamera2 import Picamera2
import time

# 카메라 초기화
picam2 = Picamera2()

# 설정
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

# 카메라 시작
picam2.start()

# 프리뷰 시간 (센서 안정화)
time.sleep(2)

# 사진 촬영
picam2.capture_file("photo.jpg")

print("사진 촬영 완료: photo.jpg")

# 카메라 정지
picam2.stop()
```

### 비디오 녹화

```python
# video.py
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time

picam2 = Picamera2()

# 비디오 설정
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

# 인코더
encoder = H264Encoder()

# 녹화 시작
picam2.start_recording(encoder, 'video.h264')

print("녹화 중... (10초)")
time.sleep(10)

# 녹화 정지
picam2.stop_recording()

print("녹화 완료: video.h264")
```

## 타임랩스

### 일정 간격으로 사진 촬영

```python
# timelapse.py
from picamera2 import Picamera2
import time
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

picam2.start()
time.sleep(2)

# 설정
INTERVAL = 60  # 60초마다
TOTAL_PHOTOS = 100  # 총 100장

print(f"타임랩스 시작: {TOTAL_PHOTOS}장, {INTERVAL}초 간격")

for i in range(TOTAL_PHOTOS):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"timelapse_{timestamp}.jpg"

    picam2.capture_file(filename)
    print(f"촬영 {i+1}/{TOTAL_PHOTOS}: {filename}")

    if i < TOTAL_PHOTOS - 1:
        time.sleep(INTERVAL)

picam2.stop()
print("타임랩스 완료!")
```

### 타임랩스 동영상 만들기

```bash
# ffmpeg 설치
sudo apt install ffmpeg

# 이미지를 동영상으로 변환
ffmpeg -framerate 30 -pattern_type glob -i 'timelapse_*.jpg' \
    -c:v libx264 -pix_fmt yuv420p timelapse.mp4
```

## 모션 감지 카메라

### PIR 센서 + 카메라

```python
# motion_camera.py
from gpiozero import MotionSensor
from picamera2 import Picamera2
from datetime import datetime
import time

# PIR 센서
pir = MotionSensor(17)

# 카메라
picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

picam2.start()
time.sleep(2)

def capture_motion():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"motion_{timestamp}.jpg"
    picam2.capture_file(filename)
    print(f"모션 감지! 사진 저장: {filename}")

print("모션 감지 카메라 시작...")
pir.when_motion = capture_motion

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("종료")
    picam2.stop()
```

## 웹 스트리밍

### Flask로 라이브 스트리밍

```python
# stream.py
from flask import Flask, Response
from picamera2 import Picamera2
import io

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def generate_frames():
    while True:
        stream = io.BytesIO()
        picam2.capture_file(stream, format='jpeg')
        stream.seek(0)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
    <head><title>라즈베리파이 카메라</title></head>
    <body>
        <h1>라이브 스트리밍</h1>
        <img src="/video_feed" width="640" height="480" />
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**접속**: `http://raspberrypi.local:5000`

## QR 코드 스캐너

```bash
pip install pyzbar pillow
```

```python
# qr_scanner.py
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from PIL import Image
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()
time.sleep(2)

print("QR 코드 스캐너 시작...")

try:
    while True:
        # 사진 촬영
        picam2.capture_file("temp.jpg")

        # QR 코드 디코딩
        img = Image.open("temp.jpg")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            print(f"QR 코드 발견: {obj.data.decode('utf-8')}")

        time.sleep(1)

except KeyboardInterrupt:
    print("종료")
    picam2.stop()
```

## 얼굴 인식

```bash
pip install opencv-python
sudo apt install python3-opencv
```

```python
# face_detection.py
from picamera2 import Picamera2
import cv2
import time

# Haar Cascade 얼굴 검출기
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()
time.sleep(2)

print("얼굴 인식 시작...")

try:
    while True:
        # 프레임 캡처
        frame = picam2.capture_array()

        # 그레이스케일 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        # 얼굴에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        print(f"검출된 얼굴: {len(faces)}개")

        # 얼굴이 검출되면 저장
        if len(faces) > 0:
            cv2.imwrite('face_detected.jpg', frame)
            print("얼굴 사진 저장!")

        time.sleep(1)

except KeyboardInterrupt:
    print("종료")
    picam2.stop()
```

## 다음 단계

➡️ [다음: 성능 최적화](../07-advanced-topics/performance-optimization.md)

## 참고 자료

- [Picamera2 문서](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [OpenCV](https://opencv.org/)
