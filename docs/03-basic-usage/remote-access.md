# 07. 원격 접속

모니터와 키보드 없이 다른 컴퓨터에서 라즈베리파이에 접속하는 다양한 방법을 배웁니다.

## 목차
- [SSH (Secure Shell)](#ssh-secure-shell)
- [VNC (Virtual Network Computing)](#vnc-virtual-network-computing)
- [원격 파일 전송](#원격-파일-전송)
- [Visual Studio Code 원격 개발](#visual-studio-code-원격-개발)
- [웹 기반 접속](#웹-기반-접속)

## SSH (Secure Shell)

### SSH란?

SSH는 네트워크를 통해 안전하게 원격 컴퓨터에 접속하는 프로토콜입니다.

**장점**:
- 암호화된 안전한 통신
- 낮은 대역폭 사용
- 명령줄 인터페이스
- 파일 전송 가능

### SSH 활성화

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

#### 방법 3: 부팅 전 설정 (헤드리스)

SD 카드의 boot 파티션에 빈 파일 `ssh` 생성:

```bash
# Windows에서
# boot 드라이브에 "ssh" 파일 생성 (확장자 없음)

# Linux/macOS에서
touch /Volumes/boot/ssh  # macOS
touch /media/username/boot/ssh  # Linux
```

### SSH 접속하기

#### 기본 접속

```bash
ssh username@hostname
# 또는
ssh username@IP주소
```

**예시**:
```bash
# hostname으로
ssh pi@raspberrypi.local

# IP 주소로
ssh pi@192.168.1.100
```

첫 접속 시:
```
The authenticity of host 'raspberrypi.local (192.168.1.100)' can't be established.
ECDSA key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

`yes` 입력 후 비밀번호 입력

#### 포트 지정

```bash
ssh -p 2222 pi@raspberrypi.local
```

#### 다른 사용자로 접속

```bash
ssh otheruser@raspberrypi.local
```

### SSH 키 인증 (비밀번호 없이 로그인)

#### 1. SSH 키 생성 (클라이언트에서)

```bash
# ED25519 키 생성 (권장)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 또는 RSA 키 (호환성 중시)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**질문에 답변**:
- 파일 위치: Enter (기본 위치 사용)
- Passphrase: 선택사항 (추가 보안층, 비워두면 자동 로그인)

#### 2. 공개 키를 라즈베리파이로 복사

```bash
# 자동 방법 (Linux/macOS)
ssh-copy-id pi@raspberrypi.local

# 수동 방법
cat ~/.ssh/id_ed25519.pub | ssh pi@raspberrypi.local "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Windows (PowerShell)
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh pi@raspberrypi.local "mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys"
```

#### 3. 권한 설정 (라즈베리파이에서)

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

#### 4. 테스트

```bash
ssh pi@raspberrypi.local
```

비밀번호 없이 접속되면 성공!

### SSH 설정 파일

클라이언트에서 `~/.ssh/config` 파일로 단축 설정:

```bash
nano ~/.ssh/config
```

내용:
```
Host mypi
    HostName raspberrypi.local
    User pi
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host pi-home
    HostName 192.168.1.100
    User pi
```

이제 간단하게 접속:
```bash
ssh mypi
ssh pi-home
```

### SSH 보안 강화

#### 1. 기본 포트 변경

```bash
sudo nano /etc/ssh/sshd_config
```

다음 줄 찾아 수정:
```
Port 2222  # 22에서 다른 번호로
```

#### 2. 루트 로그인 비활성화

```
PermitRootLogin no
```

#### 3. 비밀번호 인증 비활성화 (키 인증만)

```
PasswordAuthentication no
PubkeyAuthentication yes
```

#### 4. 설정 적용

```bash
sudo systemctl restart ssh
```

⚠️ **주의**: 설정 변경 후 현재 SSH 세션을 종료하지 말고, 새 터미널에서 접속 테스트!

### SSH 터널링

원격 포트를 로컬로 포워딩:

```bash
# 라즈베리파이의 8080 포트를 로컬 8080으로
ssh -L 8080:localhost:8080 pi@raspberrypi.local

# 이제 localhost:8080으로 접속하면 라즈베리파이의 웹서버에 연결
```

### SSH X11 포워딩

라즈베리파이의 GUI 앱을 로컬에서 실행:

```bash
ssh -X pi@raspberrypi.local

# 라즈베리파이에서 GUI 앱 실행
firefox  # 브라우저가 로컬 화면에 표시됨
```

## VNC (Virtual Network Computing)

### VNC란?

VNC는 원격 데스크톱 프로토콜로, 라즈베리파이의 GUI 화면을 원격에서 볼 수 있습니다.

**장점**:
- 그래픽 인터페이스
- 마우스/키보드 사용
- 초보자 친화적

**단점**:
- SSH보다 느림
- 더 많은 대역폭 사용

### VNC 서버 활성화

#### 방법 1: raspi-config

```bash
sudo raspi-config
# Interface Options → VNC → Enable
```

#### 방법 2: 수동 설정

```bash
sudo apt install realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced
sudo systemctl start vncserver-x11-serviced
```

### VNC 해상도 설정 (헤드리스)

모니터 없이 사용 시 해상도 설정:

```bash
sudo raspi-config
# Display Options → VNC Resolution → 1920x1080
```

또는 직접 설정:

```bash
sudo nano /boot/config.txt
```

다음 줄 추가/수정:
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82  # 1920x1080 60Hz
```

재부팅:
```bash
sudo reboot
```

### VNC 클라이언트 설치 및 접속

#### RealVNC Viewer (권장)

1. **다운로드**: [https://www.realvnc.com/download/viewer/](https://www.realvnc.com/download/viewer/)
2. **설치**
3. **실행**
4. **주소 입력**: `raspberrypi.local` 또는 IP 주소
5. **인증**: 라즈베리파이 사용자명과 비밀번호

#### 다른 VNC 클라이언트

- **TightVNC Viewer** (Windows)
- **Remmina** (Linux)
- **Screen Sharing** (macOS 내장)

### VNC 보안 설정

#### 1. 암호화 활성화 (RealVNC)

VNC 서버 설정:
```bash
sudo vncpasswd -service
```

#### 2. SSH 터널을 통한 VNC

더 안전한 방법:

```bash
# SSH 터널 생성
ssh -L 5901:localhost:5900 pi@raspberrypi.local

# VNC로 localhost:5901에 접속
```

### TigerVNC 설치 (대안)

RealVNC 대신 오픈소스 TigerVNC 사용:

```bash
# 설치
sudo apt install tigervnc-standalone-server

# VNC 비밀번호 설정
vncpasswd

# VNC 서버 시작
vncserver :1 -geometry 1920x1080 -depth 24
```

접속:
- 주소: `raspberrypi.local:1` 또는 `IP:5901`

서버 종료:
```bash
vncserver -kill :1
```

## 원격 파일 전송

### SCP (Secure Copy)

SSH를 통한 파일 전송

#### 로컬 → 라즈베리파이

```bash
# 파일 전송
scp file.txt pi@raspberrypi.local:/home/pi/

# 디렉토리 전송
scp -r mydir/ pi@raspberrypi.local:/home/pi/

# 다른 이름으로
scp file.txt pi@raspberrypi.local:/home/pi/newname.txt
```

#### 라즈베리파이 → 로컬

```bash
# 파일 받기
scp pi@raspberrypi.local:/home/pi/file.txt ./

# 디렉토리 받기
scp -r pi@raspberrypi.local:/home/pi/mydir/ ./
```

### SFTP (SSH File Transfer Protocol)

대화형 파일 전송

```bash
sftp pi@raspberrypi.local
```

**SFTP 명령어**:
```
sftp> ls                # 원격 파일 목록
sftp> lls               # 로컬 파일 목록
sftp> cd /path          # 원격 디렉토리 이동
sftp> lcd /path         # 로컬 디렉토리 이동
sftp> get file.txt      # 파일 다운로드
sftp> put file.txt      # 파일 업로드
sftp> get -r mydir/     # 디렉토리 다운로드
sftp> put -r mydir/     # 디렉토리 업로드
sftp> bye               # 종료
```

### rsync

효율적인 동기화 도구

```bash
# 디렉토리 동기화
rsync -avz /local/dir/ pi@raspberrypi.local:/remote/dir/

# 삭제된 파일도 반영
rsync -avz --delete /local/dir/ pi@raspberrypi.local:/remote/dir/

# 진행 상황 표시
rsync -avz --progress /local/dir/ pi@raspberrypi.local:/remote/dir/
```

**옵션**:
- `-a`: 아카이브 모드 (권한, 시간 유지)
- `-v`: 상세 출력
- `-z`: 압축 전송
- `--delete`: 대상에서 삭제된 파일 제거
- `--progress`: 진행률 표시
- `--dry-run`: 실제 전송 없이 테스트

### GUI 파일 관리자

#### FileZilla (크로스 플랫폼)

1. **다운로드**: [https://filezilla-project.org/](https://filezilla-project.org/)
2. **설치**
3. **접속 설정**:
   - Host: `sftp://raspberrypi.local`
   - Username: `pi`
   - Password: 비밀번호
   - Port: `22`
4. **연결**

#### WinSCP (Windows)

1. **다운로드**: [https://winscp.net/](https://winscp.net/)
2. **설치**
3. **접속 설정**
4. **드래그 앤 드롭**으로 파일 전송

## Visual Studio Code 원격 개발

### Remote-SSH 확장 설치

1. VS Code 실행
2. Extensions (Ctrl+Shift+X)
3. "Remote - SSH" 검색 및 설치 (Microsoft)

### 원격 접속

1. **F1** 키 → "Remote-SSH: Connect to Host"
2. 호스트 선택 또는 추가: `pi@raspberrypi.local`
3. 비밀번호 입력
4. 원격 폴더 열기

이제 라즈베리파이의 파일을 로컬처럼 편집 가능!

### 터미널 사용

- **View** → **Terminal** (Ctrl+`)
- 라즈베리파이의 터미널이 VS Code에서 실행됨

## 웹 기반 접속

### Cockpit

웹 기반 서버 관리 도구

#### 설치

```bash
sudo apt update
sudo apt install cockpit
sudo systemctl enable --now cockpit.socket
```

#### 접속

브라우저에서: `https://raspberrypi.local:9090`

**기능**:
- 시스템 모니터링
- 서비스 관리
- 터미널 접속
- 로그 확인

### Webmin

강력한 웹 기반 시스템 관리

#### 설치

```bash
# 저장소 추가
sudo sh -c 'echo "deb http://download.webmin.com/download/repository sarge contrib" > /etc/apt/sources.list.d/webmin.list'

# 키 추가
wget -qO - http://www.webmin.com/jcameron-key.asc | sudo apt-key add -

# 설치
sudo apt update
sudo apt install webmin
```

#### 접속

브라우저에서: `https://raspberrypi.local:10000`

## 모바일에서 접속

### SSH 클라이언트

**Android**:
- **Termux**: 완전한 터미널 환경
- **JuiceSSH**: SSH 전용
- **ConnectBot**: 오픈소스

**iOS**:
- **Termius**: SSH/SFTP 클라이언트
- **Prompt**: 프리미엄 SSH 앱
- **Blink Shell**: 전문가용

### VNC 클라이언트

**Android/iOS**:
- **RealVNC Viewer**: 공식 클라이언트
- **VNC Viewer** (RealVNC)
- **Jump Desktop**: 프리미엄 앱

## 문제 해결

### SSH 접속 안 됨

#### hostname으로 접속 안 될 때

```bash
# IP 주소 직접 사용
ssh pi@192.168.1.100

# IP 찾기 (라즈베리파이에서)
hostname -I

# 또는 공유기 관리 페이지에서 확인
```

#### Connection refused

```bash
# SSH 서비스 확인
sudo systemctl status ssh

# SSH 서비스 시작
sudo systemctl start ssh
```

#### Permission denied

- 사용자명 확인
- 비밀번호 확인
- SSH 키 권한 확인: `chmod 600 ~/.ssh/id_ed25519`

#### Host key verification failed

```bash
# 호스트 키 제거 (라즈베리파이 재설치 후)
ssh-keygen -R raspberrypi.local
# 또는
ssh-keygen -R 192.168.1.100
```

### VNC 화면이 안 나옴

#### 해상도 설정

```bash
sudo raspi-config
# Display Options → VNC Resolution
```

#### VNC 서비스 재시작

```bash
sudo systemctl restart vncserver-x11-serviced
```

### 느린 연결

#### SSH 압축 사용

```bash
ssh -C pi@raspberrypi.local
```

#### VNC 화질 낮추기

RealVNC Viewer 설정에서 Picture Quality 조정

## 원격 접속 비교

| 방법 | 용도 | 속도 | 사용 편의성 | 보안 |
|------|------|------|-------------|------|
| **SSH** | 명령줄 작업 | ⚡⚡⚡ | 중급자 이상 | ⭐⭐⭐ |
| **VNC** | GUI 작업 | ⚡⚡ | 초보자 OK | ⭐⭐ |
| **SCP/SFTP** | 파일 전송 | ⚡⚡⚡ | 중급자 이상 | ⭐⭐⭐ |
| **VS Code Remote** | 개발 | ⚡⚡ | 개발자 | ⭐⭐⭐ |
| **Webmin/Cockpit** | 시스템 관리 | ⚡⚡ | 초보자 OK | ⭐⭐ |

## 실습 예제

### 예제 1: 완전한 원격 설정

```bash
# 1. SSH 활성화
sudo raspi-config  # Interface → SSH → Enable

# 2. SSH 키 설정 (클라이언트에서)
ssh-keygen -t ed25519
ssh-copy-id pi@raspberrypi.local

# 3. SSH 접속 테스트
ssh pi@raspberrypi.local

# 4. VNC 활성화
sudo raspi-config  # Interface → VNC → Enable

# 5. 파일 전송 테스트
scp test.txt pi@raspberrypi.local:~/
```

### 예제 2: 자동 백업 스크립트

```bash
#!/bin/bash
# backup.sh - 로컬 PC에서 실행

# 라즈베리파이의 중요 파일을 백업
rsync -avz --delete \
    pi@raspberrypi.local:/home/pi/projects/ \
    ~/backups/pi-projects/

echo "Backup completed: $(date)"
```

cron으로 자동화:
```bash
# 매일 새벽 2시에 백업
0 2 * * * /home/user/backup.sh >> /var/log/pi-backup.log 2>&1
```

## 다음 단계

원격 접속 방법을 배웠습니다! 이제 GPIO를 사용한 하드웨어 제어를 시작해봅시다.

➡️ [다음: GPIO 입문](../04-hardware-projects/gpio-introduction.md)

## 참고 자료

- [SSH 공식 문서](https://www.openssh.com/manual.html)
- [RealVNC 가이드](https://help.realvnc.com/hc/en-us)
- [라즈베리파이 원격 접속 가이드](https://www.raspberrypi.com/documentation/computers/remote-access.html)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/ssh)
