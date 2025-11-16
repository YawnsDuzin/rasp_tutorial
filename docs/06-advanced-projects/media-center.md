# 12. 미디어 센터

라즈베리파이를 홈 시어터 PC로 만드는 방법을 배웁니다.

## 미디어 센터 OS

### LibreELEC

**LibreELEC**는 Kodi 전용 경량 OS입니다.

**설치**:
1. Raspberry Pi Imager 실행
2. OS 선택 → Other specific-purpose OS → Media player OS → LibreELEC
3. SD 카드에 설치

**접속**: TV에 연결 후 부팅

### OSMC

**OSMC (Open Source Media Center)**는 Kodi + Debian 기반 OS입니다.

**특징**:
- Kodi + 추가 앱 설치 가능
- 앱 스토어 제공

## Kodi 설치 (Raspberry Pi OS에서)

### 설치

```bash
sudo apt update
sudo apt install kodi
```

### 실행

```bash
kodi
```

또는 데스크톱 메뉴에서 실행

## Plex Media Server

### Plex 설치

```bash
# 의존성 설치
sudo apt install apt-transport-https

# Plex 저장소 추가
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list

# 설치
sudo apt update
sudo apt install plexmediaserver

# 서비스 시작
sudo systemctl enable plexmediaserver
sudo systemctl start plexmediaserver
```

### 설정

브라우저에서: `http://raspberrypi.local:32400/web`

### 미디어 라이브러리 설정

1. 외장 하드 마운트:
```bash
sudo mkdir /mnt/media
sudo mount /dev/sda1 /mnt/media

# 자동 마운트 설정
sudo nano /etc/fstab
# 추가: /dev/sda1 /mnt/media ntfs defaults 0 0
```

2. Plex에서 라이브러리 추가

## 음악 스트리밍: MPD

### MPD (Music Player Daemon) 설치

```bash
sudo apt install mpd mpc ncmpcpp
```

### 설정

```bash
sudo nano /etc/mpd.conf
```

```
music_directory     "/home/pi/Music"
playlist_directory  "/var/lib/mpd/playlists"
```

### 클라이언트

```bash
# 명령줄
mpc add /
mpc play

# ncmpcpp (TUI)
ncmpcpp
```

## 라디오 스트리밍

### 인터넷 라디오

```python
# radio.py
import vlc

stations = {
    'MBC': 'http://smr.hscdn.com/smr_fm.mp3',
    'SBS': 'http://sgr.hscdn.com/sgr_fm.mp3',
}

def play_radio(station_name):
    url = stations.get(station_name)
    if url:
        player = vlc.MediaPlayer(url)
        player.play()
        return player
    else:
        print("방송국을 찾을 수 없습니다.")
        return None

if __name__ == '__main__':
    print("인터넷 라디오")
    print("1. MBC")
    print("2. SBS")

    choice = input("선택: ")

    if choice == '1':
        player = play_radio('MBC')
    elif choice == '2':
        player = play_radio('SBS')

    if player:
        input("Enter를 눌러 종료...")
        player.stop()
```

## 다음 단계

➡️ [다음: IoT 프로젝트](iot-projects.md)

## 참고 자료

- [LibreELEC](https://libreelec.tv/)
- [Kodi](https://kodi.tv/)
- [Plex](https://www.plex.tv/)
