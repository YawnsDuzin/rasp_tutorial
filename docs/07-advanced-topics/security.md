# 16. 보안

라즈베리파이 시스템을 안전하게 보호하는 방법을 배웁니다.

## 기본 보안 설정

### 1. 비밀번호 변경

```bash
passwd
```

**강력한 비밀번호**:
- 최소 12자 이상
- 대소문자, 숫자, 특수문자 혼합
- 사전에 없는 단어 사용

### 2. 시스템 업데이트

```bash
# 정기적으로 실행
sudo apt update
sudo apt full-upgrade

# 자동 보안 업데이트
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. 새 사용자 생성 (pi 사용자 대신)

```bash
# 새 사용자 생성
sudo adduser newusername

# sudo 권한 부여
sudo usermod -aG sudo newusername

# 로그아웃 후 새 사용자로 로그인

# pi 사용자 삭제 (선택사항)
sudo deluser -remove-home pi
```

## SSH 보안

### 1. SSH 키 인증

**클라이언트에서**:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-copy-id username@raspberrypi.local
```

**라즈베리파이에서**:
```bash
# 비밀번호 인증 비활성화
sudo nano /etc/ssh/sshd_config
```

```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```

```bash
sudo systemctl restart ssh
```

### 2. SSH 포트 변경

```bash
sudo nano /etc/ssh/sshd_config
```

```
Port 2222  # 22 대신 다른 포트
```

```bash
sudo systemctl restart ssh
```

**접속**:
```bash
ssh -p 2222 username@raspberrypi.local
```

### 3. Fail2Ban (무차별 대입 공격 방지)

```bash
# 설치
sudo apt install fail2ban

# 설정 복사
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 설정 편집
sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = 22  # 변경한 포트 사용
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

```bash
# 서비스 시작
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 상태 확인
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## 방화벽 (UFW)

### 설치 및 설정

```bash
# 설치
sudo apt install ufw

# 기본 정책
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH 허용 (방화벽 활성화 전 필수!)
sudo ufw allow 22/tcp
# 또는 변경한 포트
sudo ufw allow 2222/tcp

# HTTP/HTTPS 허용 (웹 서버 사용 시)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# VNC 허용 (사용 시)
sudo ufw allow 5900/tcp

# 특정 IP만 허용
sudo ufw allow from 192.168.1.0/24 to any port 22

# 방화벽 활성화
sudo ufw enable

# 상태 확인
sudo ufw status verbose
```

### 규칙 관리

```bash
# 규칙 목록 (번호와 함께)
sudo ufw status numbered

# 규칙 삭제
sudo ufw delete <번호>

# 특정 규칙 삭제
sudo ufw delete allow 80/tcp

# 방화벽 비활성화
sudo ufw disable
```

## 네트워크 보안

### 1. 네트워크 스캔 방지

```bash
# iptables로 포트 스캔 차단
sudo iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
sudo iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
```

### 2. VPN 설정 (WireGuard)

```bash
# 설치
sudo apt install wireguard

# 키 생성
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey

# 설정
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
PrivateKey = <private_key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <peer_public_key>
AllowedIPs = 10.0.0.2/32
```

```bash
# VPN 시작
sudo wg-quick up wg0

# 부팅 시 자동 시작
sudo systemctl enable wg-quick@wg0
```

## 웹 애플리케이션 보안

### 1. HTTPS 설정 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx

# Nginx 설정
sudo certbot --nginx -d your-domain.com

# 자동 갱신
sudo certbot renew --dry-run
```

### 2. Flask 앱 보안

```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# HTTPS 강제 및 보안 헤더
Talisman(app, force_https=True)

# Secret Key 설정
app.secret_key = 'your-secret-key-here'  # 실제로는 환경 변수 사용

# CSRF 보호
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# SQL Injection 방지 (파라미터화된 쿼리)
import sqlite3

def safe_query(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 안전: 파라미터 바인딩
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    # 위험: 문자열 포맷팅
    # cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = cursor.fetchall()
    conn.close()
    return result
```

## 파일 및 디렉토리 권한

### 적절한 권한 설정

```bash
# 중요 파일 권한
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# 웹 디렉토리
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

# 설정 파일
sudo chmod 644 /etc/mosquitto/mosquitto.conf
```

### 파일 무결성 모니터링

```bash
# AIDE 설치
sudo apt install aide

# 데이터베이스 초기화
sudo aideinit

# 체크
sudo aide --check
```

## 로그 모니터링

### 중요 로그 확인

```bash
# 인증 로그
sudo tail -f /var/log/auth.log

# 시스템 로그
sudo journalctl -f

# SSH 실패 시도 확인
sudo grep "Failed password" /var/log/auth.log

# 마지막 로그인 확인
last
lastlog
```

### 로그 분석 자동화

```python
# log_monitor.py
import subprocess
import re

def check_failed_ssh():
    result = subprocess.run(
        ['sudo', 'grep', 'Failed password', '/var/log/auth.log'],
        capture_output=True, text=True
    )

    lines = result.stdout.strip().split('\n')

    # IP 주소 추출
    ip_pattern = r'from (\d+\.\d+\.\d+\.\d+)'
    ips = {}

    for line in lines:
        match = re.search(ip_pattern, line)
        if match:
            ip = match.group(1)
            ips[ip] = ips.get(ip, 0) + 1

    # 상위 5개 IP 출력
    sorted_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)[:5]

    print("SSH 로그인 실패 시도 (상위 5개 IP):")
    for ip, count in sorted_ips:
        print(f"  {ip}: {count}회")

if __name__ == '__main__':
    check_failed_ssh()
```

## 물리적 보안

### GPIO를 사용한 보안

```python
# intrusion_alert.py
from gpiozero import Button
import subprocess
import time

# 침입 감지 센서 (자석 센서, PIR 등)
door_sensor = Button(17)

def send_alert():
    print("⚠️ 침입 감지!")
    # 이메일 전송 또는 알림
    subprocess.run(['wall', 'Security Alert: Intrusion Detected!'])

door_sensor.when_pressed = send_alert

print("보안 시스템 가동 중...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("종료")
```

## 백업 및 복구

### 자동 백업 스크립트

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/mnt/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# 중요 디렉토리 백업
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" \
    /home/pi \
    /etc \
    /var/www

# 7일 이상 된 백업 삭제
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

echo "백업 완료: backup_$DATE.tar.gz"
```

**cron 등록**:
```bash
crontab -e
```

```
# 매일 새벽 2시 백업
0 2 * * * /home/pi/backup.sh >> /var/log/backup.log 2>&1
```

## 보안 체크리스트

### 필수 보안 조치

- [ ] 기본 비밀번호 변경
- [ ] SSH 키 인증 설정
- [ ] 비밀번호 인증 비활성화
- [ ] 정기적인 시스템 업데이트
- [ ] 방화벽(UFW) 활성화
- [ ] Fail2Ban 설치
- [ ] 불필요한 서비스 비활성화
- [ ] 정기적인 백업
- [ ] 로그 모니터링

### 추가 보안 조치

- [ ] SSH 포트 변경
- [ ] VPN 설정
- [ ] HTTPS 적용
- [ ] 파일 무결성 모니터링
- [ ] 침입 탐지 시스템
- [ ] 물리적 보안 (케이스 잠금 등)

## 보안 감사

### 정기적인 점검

```bash
# 열려 있는 포트 확인
sudo netstat -tuln
sudo ss -tuln

# 실행 중인 서비스
systemctl list-units --type=service --state=running

# 설치된 패키지 확인
dpkg -l

# 수상한 프로세스 확인
ps aux | grep -v grep
```

### 보안 스캔 도구

```bash
# Lynis 설치 (보안 감사 도구)
sudo apt install lynis

# 시스템 감사
sudo lynis audit system
```

## 침해 사고 대응

### 의심스러운 활동 발견 시

1. **네트워크 연결 차단**:
```bash
sudo systemctl stop networking
```

2. **로그 백업**:
```bash
sudo cp -r /var/log /backup/logs_$(date +%Y%m%d)
```

3. **의심스러운 프로세스 종료**:
```bash
sudo kill -9 <PID>
```

4. **시스템 재설치 고려**

## 참고 자료

- [라즈베리파이 보안 가이드](https://www.raspberrypi.com/documentation/computers/configuration.html#securing-your-raspberry-pi)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS 벤치마크](https://www.cisecurity.org/benchmark/debian_linux/)

---

**축하합니다!** 🎉

라즈베리파이 완벽 가이드를 모두 완료하셨습니다. 이제 다양한 프로젝트를 직접 만들어보세요!
