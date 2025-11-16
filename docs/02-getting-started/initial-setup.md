# 05. 초기 설정

라즈베리파이 OS를 설치한 후 필요한 초기 설정과 최적화 방법을 안내합니다.

## 개요

이 섹션에서 다룰 내용:
- 시스템 업데이트
- 지역 및 언어 설정
- 네트워크 설정
- SSH 설정
- VNC 설정
- 시스템 구성 도구 사용
- 기본 보안 설정

## 1. 시스템 업데이트

### 1.1 패키지 목록 업데이트

터미널을 열고 다음 명령어를 실행합니다:

```bash
sudo apt update
```

이 명령어는:
- 사용 가능한 패키지 목록을 최신 상태로 업데이트
- 설치 가능한 소프트웨어 정보 갱신

### 1.2 시스템 업그레이드

```bash
sudo apt full-upgrade -y
```

이 명령어는:
- 설치된 모든 패키지를 최신 버전으로 업그레이드
- 시스템 보안 패치 적용
- 새로운 기능 추가

⏱️ **소요 시간**: 5~20분 (네트워크 속도와 업데이트 양에 따라)

💡 **옵션**:
- `-y`: 모든 질문에 자동으로 "yes" 응답
- `apt upgrade` vs `apt full-upgrade`:
  - `upgrade`: 안전한 업그레이드만
  - `full-upgrade`: 의존성 해결하며 전체 업그레이드 (권장)

### 1.3 불필요한 패키지 제거

```bash
sudo apt autoremove -y
sudo apt autoclean
```

- `autoremove`: 더 이상 필요 없는 의존성 패키지 제거
- `autoclean`: 다운로드한 패키지 파일 정리

### 1.4 펌웨어 업데이트 (선택사항)

```bash
sudo rpi-update
```

⚠️ **주의**:
- 최신 펌웨어로 업데이트 (실험적 기능 포함 가능)
- 문제 발생 가능성 있으므로 신중히 사용
- 일반적으로 `apt full-upgrade`로 충분

### 1.5 재부팅

주요 업데이트 후 재부팅:

```bash
sudo reboot
```

## 2. Raspberry Pi 설정 도구

### 2.1 raspi-config 실행

라즈베리파이의 종합 설정 도구:

```bash
sudo raspi-config
```

텍스트 기반 메뉴 인터페이스가 나타납니다.

**방향키**: 이동
**Enter**: 선택
**Tab**: 버튼 간 이동
**Esc**: 뒤로/취소

### 2.2 주요 설정 항목

#### System Options

**S1 Wireless LAN**
- Wi-Fi 네트워크 설정
- SSID와 비밀번호 입력

**S3 Password**
- 사용자 비밀번호 변경
- 보안을 위해 기본 비밀번호 변경 권장

**S4 Hostname**
- 네트워크에서 사용할 이름 설정
- 기본값: `raspberrypi`
- 예: `mypi`, `homeserver` 등

**S5 Boot / Auto Login**
- Desktop 자동 로그인 설정
- CLI 또는 Desktop 선택

**S6 Network at Boot**
- 부팅 시 네트워크 연결 대기 여부

**S7 Splash Screen**
- 부팅 시 로고 화면 표시 여부

#### Interface Options

**I1 SSH**
- SSH 서버 활성화/비활성화
- 원격 접속을 위해 **활성화 권장** ✅

**I2 VNC**
- VNC 서버 활성화/비활성화
- 원격 데스크톱을 위해 활성화

**I3 SPI**
- SPI 인터페이스 활성화
- 특정 센서/디스플레이 사용 시 필요

**I4 I2C**
- I2C 인터페이스 활성화
- 많은 센서가 I2C 사용

**I5 Serial Port**
- 시리얼 포트 활성화
- UART 통신 필요 시

**I6 1-Wire**
- 1-Wire 인터페이스 (온도 센서 등)

**I7 Remote GPIO**
- 원격 GPIO 제어 활성화

#### Localisation Options

**L1 Locale**
- 언어 및 문자 인코딩 설정
- 추천:
  - `en_US.UTF-8 UTF-8` (영어)
  - `ko_KR.UTF-8 UTF-8` (한국어, 선택사항)
- 기본 locale: `en_US.UTF-8`

**L2 Timezone**
- 시간대 설정
- Asia → Seoul 선택

**L3 Keyboard**
- 키보드 레이아웃 설정
- Generic 105-key PC
- Other → English (US) (일반적)
- 또는 Korean

**L4 WLAN Country**
- Wi-Fi 국가 코드
- **KR (Korea)** 선택 ✅
- 필수 설정 (Wi-Fi 작동에 필요)

#### Performance Options

**P1 Overclock**
- CPU 오버클러킹
- ⚠️ 발열 및 안정성 고려

**P2 GPU Memory**
- GPU에 할당할 메모리
- Desktop: 128MB~256MB
- Headless/Server: 16MB~64MB

**P3 Overlay File System**
- 읽기 전용 파일 시스템
- SD 카드 수명 연장

**P4 Fan**
- 공식 쿨러 설정 (Pi 4/5)

#### Advanced Options

**A1 Expand Filesystem**
- SD 카드 전체 공간 사용
- 보통 자동으로 되지만, 안 된 경우 수동 실행

**A3 Network Interface Names**
- 네트워크 인터페이스 이름 방식

**A4 Network Proxy Settings**
- 프록시 서버 설정

### 2.3 설정 완료

- `<Finish>` 선택
- 재부팅 요청 시 `<Yes>` 선택

## 3. 네트워크 설정

### 3.1 Wi-Fi 설정 (GUI)

Desktop 환경에서:

1. 우측 상단의 네트워크 아이콘 클릭
2. Wi-Fi 네트워크 선택
3. 비밀번호 입력

### 3.2 Wi-Fi 설정 (CLI)

```bash
# Wi-Fi 설정
sudo raspi-config
# System Options → Wireless LAN

# 또는 직접 편집
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

다음 내용 추가:

```
network={
    ssid="WiFi이름"
    psk="비밀번호"
}
```

저장 후:

```bash
sudo wpa_cli -i wlan0 reconfigure
```

### 3.3 고정 IP 설정

#### 방법 1: dhcpcd 사용 (권장)

```bash
sudo nano /etc/dhcpcd.conf
```

파일 끝에 추가:

```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8

interface wlan0
static ip_address=192.168.1.101/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

**설명**:
- `eth0`: 유선 이더넷
- `wlan0`: 무선 Wi-Fi
- `ip_address`: 원하는 고정 IP/서브넷
- `routers`: 게이트웨이 (보통 공유기 IP)
- `domain_name_servers`: DNS 서버

저장 후 재부팅:

```bash
sudo reboot
```

### 3.4 네트워크 확인

```bash
# IP 주소 확인
ip addr show

# 또는
hostname -I

# 네트워크 연결 테스트
ping -c 4 8.8.8.8

# DNS 테스트
ping -c 4 google.com
```

## 4. SSH 설정

### 4.1 SSH 활성화

#### 방법 1: raspi-config

```bash
sudo raspi-config
# Interface Options → SSH → Enable
```

#### 방법 2: systemctl

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

### 4.2 SSH 접속 테스트

다른 컴퓨터에서:

```bash
ssh username@raspberrypi.local
# 또는
ssh username@192.168.1.100
```

- `username`: 설정한 사용자명
- `raspberrypi.local`: hostname (또는 IP 주소)

처음 접속 시:
- 핑거프린트 확인 메시지: `yes` 입력
- 비밀번호 입력

### 4.3 SSH 보안 강화

#### 비밀번호 인증 대신 SSH 키 사용

**클라이언트(접속하는 PC)에서**:

```bash
# SSH 키 생성 (없는 경우)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개 키를 라즈베리파이로 복사
ssh-copy-id username@raspberrypi.local
```

**라즈베리파이에서**:

```bash
# 비밀번호 인증 비활성화 (선택사항, 주의!)
sudo nano /etc/ssh/sshd_config
```

다음 줄 찾아서 수정:

```
PasswordAuthentication no
PubkeyAuthentication yes
```

저장 후 SSH 재시작:

```bash
sudo systemctl restart ssh
```

⚠️ **경고**: 비밀번호 인증을 비활성화하기 전에 SSH 키로 접속이 되는지 확인!

## 5. VNC 설정

### 5.1 VNC 활성화

```bash
sudo raspi-config
# Interface Options → VNC → Enable
```

### 5.2 VNC 해상도 설정

헤드리스(모니터 없이) 환경에서:

```bash
sudo raspi-config
# Display Options → VNC Resolution → 1920x1080 (원하는 해상도)
```

### 5.3 VNC 클라이언트 설치

다른 컴퓨터에서:

- **RealVNC Viewer** 다운로드: [https://www.realvnc.com/download/viewer/](https://www.realvnc.com/download/viewer/)
- 설치 후 실행
- 주소 입력: `raspberrypi.local` 또는 IP 주소
- 사용자명과 비밀번호로 로그인

### 5.4 대안: TigerVNC

```bash
# 라즈베리파이에 TigerVNC 설치
sudo apt install tigervnc-standalone-server tigervnc-common

# VNC 서버 비밀번호 설정
vncpasswd

# VNC 서버 시작
vncserver :1 -geometry 1920x1080 -depth 24
```

## 6. 기본 보안 설정

### 6.1 비밀번호 변경

```bash
passwd
```

강력한 비밀번호로 변경하세요:
- 최소 8자 이상
- 대소문자, 숫자, 특수문자 조합

### 6.2 소프트웨어 자동 업데이트 (선택사항)

#### unattended-upgrades 설치

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

"Yes" 선택하여 자동 보안 업데이트 활성화

### 6.3 방화벽 설정 (선택사항)

#### UFW (Uncomplicated Firewall) 설치

```bash
sudo apt install ufw

# SSH 허용 (방화벽 활성화 전 필수!)
sudo ufw allow 22/tcp

# VNC 허용 (사용 시)
sudo ufw allow 5900/tcp

# 방화벽 활성화
sudo ufw enable

# 상태 확인
sudo ufw status
```

### 6.4 Fail2Ban 설치 (무차별 대입 공격 방지)

```bash
sudo apt install fail2ban

# 서비스 시작 및 활성화
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 상태 확인
sudo fail2ban-client status
```

## 7. 유용한 도구 설치

### 7.1 필수 도구

```bash
sudo apt install -y \
    git \
    vim \
    curl \
    wget \
    htop \
    tree \
    net-tools
```

**설명**:
- `git`: 버전 관리
- `vim`: 텍스트 에디터
- `curl`, `wget`: 파일 다운로드
- `htop`: 시스템 모니터
- `tree`: 디렉토리 구조 보기
- `net-tools`: 네트워크 도구 (ifconfig 등)

### 7.2 Python 도구

```bash
sudo apt install -y \
    python3-pip \
    python3-venv
```

### 7.3 개발 도구

```bash
sudo apt install -y \
    build-essential \
    cmake
```

## 8. 시스템 정보 확인

### 8.1 하드웨어 정보

```bash
# CPU 정보
lscpu

# 메모리 정보
free -h

# 디스크 정보
df -h

# 온도 확인
vcgencmd measure_temp

# 전압 확인
vcgencmd measure_volts

# 클럭 속도 확인
vcgencmd measure_clock arm
```

### 8.2 소프트웨어 정보

```bash
# OS 버전
cat /etc/os-release

# 커널 버전
uname -r

# 라즈베리파이 모델
cat /proc/device-tree/model
```

## 9. 성능 모니터링

### 9.1 실시간 모니터링

```bash
# CPU/메모리 사용량
htop

# 디스크 I/O
iotop

# 네트워크
iftop
```

### 9.2 온도 모니터링

```bash
# 실시간 온도 확인
watch -n 1 vcgencmd measure_temp
```

**안전 온도**:
- 정상: 40~60°C
- 주의: 60~75°C
- 위험: 75°C 이상 (스로틀링 발생)

## 10. 백업 및 복원

### 10.1 SD 카드 백업

설정을 완료한 후 SD 카드를 백업하는 것이 좋습니다.

#### 방법 1: SD 카드 이미지 백업 (PC에서)

```bash
# Linux/macOS
sudo dd if=/dev/sdX of=~/raspberry-backup.img bs=4M status=progress

# 압축하여 저장
sudo dd if=/dev/sdX bs=4M status=progress | gzip > ~/raspberry-backup.img.gz
```

#### 방법 2: 파일 백업 (라즈베리파이에서)

```bash
# 중요 설정 파일 백업
tar -czf ~/config-backup.tar.gz \
    /etc/network/ \
    /etc/wpa_supplicant/ \
    /home/username/ \
    /etc/hostname \
    /etc/hosts
```

### 10.2 자동 백업 스크립트 (선택사항)

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
tar -czf /backup/home-$DATE.tar.gz /home/username/
find /backup -name "home-*.tar.gz" -mtime +7 -delete
```

## 체크리스트

설정 완료 후 확인:

- [ ] 시스템 업데이트 완료
- [ ] 시간대 설정 (Asia/Seoul)
- [ ] Wi-Fi/네트워크 연결
- [ ] SSH 활성화 및 테스트
- [ ] (선택) VNC 활성화 및 테스트
- [ ] 비밀번호 변경
- [ ] hostname 설정
- [ ] 필수 도구 설치
- [ ] 백업 완료

## 다음 단계

기본 설정을 완료했습니다! 이제 리눅스 기본 명령어를 배워봅시다.

➡️ [다음: 리눅스 기초 명령어](../03-basic-usage/linux-basics.md)

## 참고 자료

- [라즈베리파이 공식 설정 가이드](https://www.raspberrypi.com/documentation/computers/configuration.html)
- [raspi-config 문서](https://www.raspberrypi.com/documentation/computers/configuration.html#raspi-config)
- [네트워크 설정](https://www.raspberrypi.com/documentation/computers/configuration.html#networking)
- [원격 접속](https://www.raspberrypi.com/documentation/computers/remote-access.html)
