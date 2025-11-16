# 11. 웹 서버 구축

라즈베리파이에서 웹 서버를 구축하고 Flask를 사용하여 웹 애플리케이션을 만드는 방법을 배웁니다.

## 웹 서버 종류

### 정적 웹 서버
- **Apache**: 가장 인기 있는 웹 서버
- **Nginx**: 가볍고 빠른 웹 서버

### 동적 웹 애플리케이션
- **Flask**: 경량 Python 웹 프레임워크 (권장)
- **Django**: 풀스택 Python 웹 프레임워크
- **Node.js**: JavaScript 기반 웹 서버

## Flask 웹 서버

### Flask 설치

```bash
pip install flask
```

### 기본 Flask 앱

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>안녕하세요, 라즈베리파이!</h1>'

@app.route('/about')
def about():
    return '<h1>소개 페이지</h1><p>라즈베리파이 웹 서버입니다.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**실행**:
```bash
python3 app.py
```

**접속**: 브라우저에서 `http://raspberrypi.local:5000`

### HTML 템플릿 사용

**디렉토리 구조**:
```
myapp/
├── app.py
└── templates/
    ├── index.html
    └── about.html
```

**app.py**:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='홈')

@app.route('/about')
def about():
    return render_template('about.html', title='소개')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**templates/index.html**:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - 라즈베리파이</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { color: #c51a4a; }
    </style>
</head>
<body>
    <h1>라즈베리파이 웹 서버</h1>
    <p>Flask를 사용한 웹 애플리케이션입니다.</p>
    <nav>
        <a href="/">홈</a> |
        <a href="/about">소개</a> |
        <a href="/sensors">센서 데이터</a>
    </nav>
</body>
</html>
```

## 센서 데이터 웹 대시보드

### 실시간 센서 모니터링

```python
from flask import Flask, render_template, jsonify
import board
import adafruit_dht
import time

app = Flask(__name__)

# DHT22 센서
dht_device = adafruit_dht.DHT22(board.D4)

def get_sensor_data():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return {
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    except RuntimeError:
        return None

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/sensor')
def api_sensor():
    data = get_sensor_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Sensor read error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**templates/dashboard.html**:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>센서 대시보드</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .sensor-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .sensor-value {
            font-size: 48px;
            font-weight: bold;
            color: #c51a4a;
        }
        .sensor-label {
            font-size: 18px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>실시간 센서 모니터링</h1>

    <div class="sensor-card">
        <div class="sensor-label">온도</div>
        <div class="sensor-value" id="temperature">--</div>
        <div class="sensor-label">°C</div>
    </div>

    <div class="sensor-card">
        <div class="sensor-label">습도</div>
        <div class="sensor-value" id="humidity">--</div>
        <div class="sensor-label">%</div>
    </div>

    <div class="sensor-card">
        <div class="sensor-label">마지막 업데이트</div>
        <div id="timestamp">--</div>
    </div>

    <script>
        function updateSensorData() {
            fetch('/api/sensor')
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        document.getElementById('temperature').textContent = data.temperature;
                        document.getElementById('humidity').textContent = data.humidity;
                        document.getElementById('timestamp').textContent = data.timestamp;
                    }
                })
                .catch(error => console.error('Error:', error));
        }

        // 5초마다 업데이트
        setInterval(updateSensorData, 5000);

        // 페이지 로드 시 즉시 업데이트
        updateSensorData();
    </script>
</body>
</html>
```

## GPIO 제어 웹 인터페이스

### LED 제어 웹 앱

```python
from flask import Flask, render_template, request, jsonify
from gpiozero import LED

app = Flask(__name__)

# GPIO 핀 설정
led = LED(17)

@app.route('/')
def index():
    return render_template('led_control.html')

@app.route('/led/<action>')
def led_action(action):
    if action == 'on':
        led.on()
        return jsonify({'status': 'LED ON'})
    elif action == 'off':
        led.off()
        return jsonify({'status': 'LED OFF'})
    elif action == 'toggle':
        led.toggle()
        status = 'ON' if led.is_lit else 'OFF'
        return jsonify({'status': f'LED {status}'})
    else:
        return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        led.close()
```

**templates/led_control.html**:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>LED 제어</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        button {
            font-size: 24px;
            padding: 20px 40px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .on-btn { background-color: #4CAF50; color: white; }
        .off-btn { background-color: #f44336; color: white; }
        .toggle-btn { background-color: #2196F3; color: white; }
        #status {
            font-size: 32px;
            margin-top: 30px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>LED 제어 패널</h1>

    <button class="on-btn" onclick="controlLED('on')">켜기</button>
    <button class="off-btn" onclick="controlLED('off')">끄기</button>
    <button class="toggle-btn" onclick="controlLED('toggle')">토글</button>

    <div id="status"></div>

    <script>
        function controlLED(action) {
            fetch(`/led/${action}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').textContent = data.status || data.error;
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
```

## 데이터 로깅 및 그래프

### Chart.js를 사용한 그래프

```python
from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('graph.html')

@app.route('/api/history')
def api_history():
    conn = sqlite3.connect('sensors.db')
    cursor = conn.cursor()

    # 최근 24시간 데이터
    yesterday = datetime.now() - timedelta(days=1)

    cursor.execute('''
        SELECT timestamp, temperature, humidity
        FROM sensor_readings
        WHERE timestamp > ?
        ORDER BY timestamp ASC
    ''', (yesterday.isoformat(),))

    rows = cursor.fetchall()
    conn.close()

    data = {
        'timestamps': [row[0] for row in rows],
        'temperatures': [row[1] for row in rows],
        'humidity': [row[2] for row in rows]
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**templates/graph.html**:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>센서 데이터 그래프</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>24시간 센서 데이터</h1>
    <canvas id="tempChart" width="800" height="400"></canvas>

    <script>
        fetch('/api/history')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('tempChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.timestamps,
                        datasets: [{
                            label: '온도 (°C)',
                            data: data.temperatures,
                            borderColor: 'rgb(255, 99, 132)',
                            tension: 0.1
                        }, {
                            label: '습도 (%)',
                            data: data.humidity,
                            borderColor: 'rgb(54, 162, 235)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
    </script>
</body>
</html>
```

## 백그라운드 서비스로 실행

### systemd 서비스 생성

```bash
sudo nano /etc/systemd/system/flask-app.service
```

**내용**:
```ini
[Unit]
Description=Flask Web Application
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/myapp
ExecStart=/usr/bin/python3 /home/pi/myapp/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**서비스 시작**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
sudo systemctl status flask-app
```

## 보안 강화

### HTTPS 설정 (자체 서명 인증서)

```bash
# OpenSSL로 인증서 생성
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365
```

**Flask에서 HTTPS 사용**:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,
            ssl_context=('cert.pem', 'key.pem'))
```

### 인증 추가

```bash
pip install flask-login
```

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)

# 간단한 사용자 (실제로는 데이터베이스 사용)
users = {'admin': {'password': 'password123'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users and request.form['password'] == users[username]['password']:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('protected'))

    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username"/>
            <input type="password" name="password" placeholder="Password"/>
            <input type="submit" value="Login"/>
        </form>
    '''

@app.route('/protected')
@login_required
def protected():
    return 'Logged in successfully!'

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## 다음 단계

웹 서버 구축 방법을 배웠습니다! 이제 고급 프로젝트를 시작해봅시다.

➡️ [다음: IoT 프로젝트](../06-advanced-projects/iot-projects.md)

## 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Chart.js 문서](https://www.chartjs.org/)
