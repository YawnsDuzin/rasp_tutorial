# 04. OS 설치하기

Raspberry Pi Imager를 사용하여 라즈베리파이 OS를 설치하는 방법을 단계별로 안내합니다.

## 준비물 체크리스트

시작하기 전에 다음 항목을 준비하세요:

- [ ] 라즈베리파이 보드
- [ ] MicroSD 카드 (16GB 이상, Class 10)
- [ ] MicroSD 카드 리더기
- [ ] PC (Windows, macOS, 또는 Linux)
- [ ] 인터넷 연결

## 설치 방법 개요

라즈베리파이 OS를 설치하는 방법은 크게 두 가지입니다:

1. **Raspberry Pi Imager 사용 (권장)** ⭐
   - 공식 도구
   - 가장 쉽고 안전
   - 초보자에게 적합

2. **수동 이미지 다운로드 및 쓰기**
   - 고급 사용자용
   - 특수한 이미지 필요 시

이 가이드에서는 **Raspberry Pi Imager**를 사용하는 방법을 설명합니다.

## 단계 1: Raspberry Pi Imager 다운로드

### 1.1 공식 웹사이트 방문

[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

### 1.2 운영체제별 다운로드

- **Windows**: "Download for Windows" 클릭
- **macOS**: "Download for macOS" 클릭
- **Ubuntu/Debian**: "Download for Ubuntu" 클릭

### 1.3 설치

#### Windows
1. 다운로드한 `.exe` 파일 실행
2. "Install" 클릭
3. 설치 완료 후 "Finish" 클릭

#### macOS
1. 다운로드한 `.dmg` 파일 열기
2. "Raspberry Pi Imager" 앱을 Applications 폴더로 드래그
3. Applications에서 실행

#### Linux
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install rpi-imager

# Fedora
sudo dnf install rpi-imager

# Arch Linux
yay -S rpi-imager
```

## 단계 2: SD 카드 준비

### 2.1 SD 카드를 PC에 연결

- MicroSD 카드를 카드 리더기에 삽입
- 카드 리더기를 PC의 USB 포트에 연결

### 2.2 SD 카드 백업 (기존 데이터가 있는 경우)

⚠️ **경고**: 설치 과정에서 SD 카드의 모든 데이터가 삭제됩니다!

중요한 데이터가 있다면 미리 백업하세요.

## 단계 3: Raspberry Pi Imager 사용

### 3.1 Raspberry Pi Imager 실행

- Windows: 시작 메뉴에서 "Raspberry Pi Imager" 검색
- macOS: Applications 폴더에서 실행
- Linux: 터미널에서 `rpi-imager` 또는 애플리케이션 메뉴에서 실행

### 3.2 라즈베리파이 기기 선택

1. **"CHOOSE DEVICE"** 버튼 클릭
2. 사용 중인 라즈베리파이 모델 선택:
   - Raspberry Pi 5
   - Raspberry Pi 4
   - Raspberry Pi 3
   - Raspberry Pi Zero 2 W
   - 등등

💡 **팁**: 정확한 모델을 선택하면 호환 가능한 OS만 표시됩니다.

### 3.3 운영체제 선택

1. **"CHOOSE OS"** 버튼 클릭
2. 원하는 OS 선택:

#### 추천 옵션 (입문자)
- **Raspberry Pi OS (64-bit)**
  - 최신 라즈베리파이(Pi 4/5)용 권장
  - Desktop 환경 포함

- **Raspberry Pi OS (32-bit)**
  - 구형 모델(Pi 3 이하) 또는 호환성 중시

- **Raspberry Pi OS (Legacy)**
  - 구형 소프트웨어 호환성 필요 시

#### 기타 옵션
- **Raspberry Pi OS (other)**
  - Lite (GUI 없음)
  - Full (추가 소프트웨어 포함)

- **Other general-purpose OS**
  - Ubuntu Desktop/Server
  - Debian
  - 등등

- **Other specific-purpose OS**
  - LibreELEC (미디어 센터)
  - RetroPie (게임)
  - 등등

💡 **초보자 추천**: "Raspberry Pi OS (64-bit)" 선택

### 3.4 SD 카드 선택

1. **"CHOOSE STORAGE"** 버튼 클릭
2. 연결된 SD 카드 선택

⚠️ **주의**:
- 올바른 드라이브를 선택했는지 확인!
- 잘못된 드라이브 선택 시 데이터 손실 가능

### 3.5 고급 설정 (권장)

설치 전에 미리 설정을 구성할 수 있습니다. 이렇게 하면 첫 부팅 시 편리합니다.

1. **"NEXT"** 버튼 클릭
2. "Would you like to apply OS customisation settings?" 팝업에서 **"EDIT SETTINGS"** 선택

#### General 탭 설정

**hostname 설정**
- 네트워크에서 라즈베리파이를 식별하는 이름
- 기본값: `raspberrypi.local`
- 예: `mypi.local`

**사용자 이름 및 비밀번호**
- Username: 원하는 사용자 이름 (기본: `pi`)
- Password: 안전한 비밀번호 설정
- ✅ 반드시 설정 권장 (보안)

**Wi-Fi 설정** (선택사항)
- ✅ Configure wireless LAN 체크
- SSID: Wi-Fi 네트워크 이름
- Password: Wi-Fi 비밀번호
- Wireless LAN country: KR (Korea)

**로케일 설정**
- Time zone: Asia/Seoul
- Keyboard layout: us (또는 kr)

#### Services 탭 설정

**SSH 활성화** (권장)
- ✅ Enable SSH 체크
- 원격 접속을 위해 필요
- "Use password authentication" 선택 (초보자)

💡 **팁**: 헤드리스(모니터 없이) 설정하려면 SSH와 Wi-Fi를 반드시 활성화하세요!

#### Options 탭 설정

- ✅ Eject media when finished (완료 후 자동 꺼내기)
- ✅ Enable telemetry (선택사항 - 사용 통계 전송)

3. **"SAVE"** 클릭하여 설정 저장

### 3.6 이미지 쓰기

1. **"YES"** 클릭하여 설정 적용 확인
2. 데이터 삭제 경고 확인 후 **"YES"** 클릭
3. 관리자 권한 요청 시 승인 (Windows/macOS)

이제 이미지 쓰기가 시작됩니다:

- **Writing...**: OS 이미지를 SD 카드에 쓰는 중
- **Verifying...**: 쓰기가 올바르게 되었는지 확인 중

⏱️ **소요 시간**: 약 5~15분 (SD 카드 속도에 따라 다름)

### 3.7 완료

"Write Successful" 메시지가 나타나면 완료!

1. **"CONTINUE"** 클릭
2. SD 카드를 안전하게 제거

## 단계 4: 라즈베리파이에 SD 카드 삽입

### 4.1 SD 카드 삽입

1. 라즈베리파이의 전원이 **꺼져 있는지** 확인
2. MicroSD 카드를 라즈베리파이 하단의 슬롯에 삽입
   - 금속 접점이 보드 쪽을 향하도록
   - 딸깍 소리가 날 때까지 밀어 넣기

### 4.2 주변기기 연결

첫 부팅을 위해 다음을 연결합니다:

**모니터 사용 시**:
1. HDMI 케이블로 모니터 연결
2. USB 키보드 연결
3. USB 마우스 연결 (선택)
4. 이더넷 케이블 연결 (선택)

**헤드리스 설정 시** (SSH 사용):
- 이더넷 케이블만 연결 (또는 Wi-Fi 사전 설정)

### 4.3 전원 연결

1. 전원 어댑터를 라즈베리파이에 연결
2. 전원 어댑터를 콘센트에 연결

🔴 **전원 LED**가 켜지면서 부팅이 시작됩니다.

## 단계 5: 첫 부팅

### 5.1 부팅 과정

첫 부팅 시:
- 화면에 많은 텍스트가 표시됨 (부팅 로그)
- 자동으로 설정 적용
- 재부팅 1~2회 가능

⏱️ **첫 부팅 시간**: 약 1~3분

### 5.2 데스크톱 환경 (GUI)

Raspberry Pi OS Desktop 버전을 설치했다면:

1. **데스크톱 화면** 표시
2. 이미 설정한 경우 바로 사용 가능
3. 설정하지 않았다면 **Setup Wizard** 실행

#### Setup Wizard (고급 설정을 건너뛴 경우)

1. **Welcome**: Next 클릭
2. **Set Country**:
   - Country: Korea
   - Language: Korean (또는 English)
   - Timezone: Seoul
   - ✅ Use English language
   - ✅ Use US keyboard
3. **Create User**: 사용자명과 비밀번호 설정
4. **Set Up Screen**: 화면 테두리 조정 (필요 시)
5. **Select WiFi Network**: Wi-Fi 네트워크 선택 및 비밀번호 입력
6. **Update Software**: 시스템 업데이트 (권장)
7. **Setup Complete**: Restart 클릭

### 5.3 Lite 버전 (CLI)

Raspberry Pi OS Lite를 설치했다면:

1. 로그인 프롬프트 표시
```
raspberrypi login:
```

2. 설정한 사용자명과 비밀번호로 로그인

3. 터미널 환경에서 시작

## 단계 6: 초기 확인

### 6.1 시스템 정보 확인

터미널을 열고 다음 명령어 실행:

```bash
# OS 버전 확인
cat /etc/os-release

# 라즈베리파이 모델 확인
cat /proc/device-tree/model

# 커널 버전 확인
uname -a
```

### 6.2 네트워크 확인

```bash
# IP 주소 확인
hostname -I

# 인터넷 연결 확인
ping -c 4 google.com
```

### 6.3 저장공간 확인

```bash
# 디스크 사용량 확인
df -h
```

SD 카드 전체 용량이 사용 가능한지 확인하세요.

## 대체 방법: 수동 설치 (고급)

Raspberry Pi Imager 대신 수동으로 설치하려면:

### Windows: Rufus, Win32 Disk Imager
### macOS/Linux: dd 명령어

```bash
# 이미지 다운로드
wget https://downloads.raspberrypi.org/raspios_arm64/images/...

# 압축 해제
unzip 2024-xx-xx-raspios-*.zip

# SD 카드에 쓰기 (macOS/Linux)
sudo dd if=2024-xx-xx-raspios-*.img of=/dev/sdX bs=4M status=progress
sudo sync
```

⚠️ **주의**: `/dev/sdX`를 올바른 디바이스로 교체하세요!

## 문제 해결

### SD 카드가 인식되지 않음
- 카드 리더기 다시 연결
- 다른 USB 포트 시도
- 다른 카드 리더기 사용

### 쓰기 실패
- SD 카드의 쓰기 보호 스위치 확인
- SD 카드 포맷 후 재시도
- 다른 SD 카드 사용

### 부팅되지 않음
- 전원 어댑터 확인 (충분한 전류)
- SD 카드 제대로 삽입되었는지 확인
- 다른 SD 카드로 재설치
- 빨간색 LED만 켜지고 녹색 LED가 안 켜지면 SD 카드 문제

### 화면에 아무것도 표시되지 않음
- HDMI 케이블 확인
- 모니터 입력 소스 확인
- 다른 HDMI 포트 시도 (Pi 4/5는 2개 포트)

### Wi-Fi 연결 안 됨
- Wi-Fi 국가 설정 확인 (KR)
- SSID와 비밀번호 정확한지 확인
- 2.4GHz 네트워크 사용 (5GHz는 모델에 따라 다름)

## 백업 방법

설정을 완료한 후 SD 카드를 백업하는 것이 좋습니다.

### Windows: Win32 Disk Imager
- "Read" 기능으로 이미지 생성

### macOS/Linux
```bash
sudo dd if=/dev/sdX of=~/backup-raspberrypi.img bs=4M status=progress
```

## 다음 단계

OS 설치가 완료되었습니다! 이제 초기 설정을 진행합니다.

➡️ [다음: 초기 설정](initial-setup.md)

## 참고 자료

- [Raspberry Pi Imager 공식 가이드](https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager)
- [고급 설정 옵션](https://www.raspberrypi.com/documentation/computers/getting-started.html#advanced-options)
- [헤드리스 설정](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)
