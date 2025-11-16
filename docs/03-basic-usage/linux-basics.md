# 06. 리눅스 기초 명령어

라즈베리파이를 효과적으로 사용하기 위해 필요한 리눅스 기본 명령어를 배웁니다.

## 목차
- [터미널 기초](#터미널-기초)
- [파일 시스템 탐색](#파일-시스템-탐색)
- [파일 및 디렉토리 관리](#파일-및-디렉토리-관리)
- [파일 내용 보기 및 편집](#파일-내용-보기-및-편집)
- [권한 관리](#권한-관리)
- [프로세스 관리](#프로세스-관리)
- [패키지 관리](#패키지-관리)
- [네트워크 명령어](#네트워크-명령어)
- [시스템 정보](#시스템-정보)
- [유용한 팁](#유용한-팁)

## 터미널 기초

### 터미널이란?

터미널(Terminal)은 텍스트 기반으로 컴퓨터와 상호작용하는 인터페이스입니다.

### 터미널 열기

**Desktop 환경**:
- 상단 메뉴: `Menu` → `Accessories` → `Terminal`
- 단축키: `Ctrl + Alt + T`

**SSH 원격 접속**:
- 이미 터미널 환경

### 프롬프트 이해하기

```bash
pi@raspberrypi:~ $
```

**구성요소**:
- `pi`: 현재 사용자명
- `raspberrypi`: 호스트명
- `~`: 현재 디렉토리 (`~`는 홈 디렉토리)
- `$`: 일반 사용자 (루트는 `#`)

### 기본 규칙

1. **대소문자 구분**: `File.txt`와 `file.txt`는 다른 파일
2. **공백 주의**: 파일명에 공백이 있으면 `""`로 감싸거나 `\` 사용
3. **자동 완성**: `Tab` 키로 명령어/파일명 자동 완성
4. **명령어 취소**: `Ctrl + C`
5. **명령어 히스토리**: `↑`, `↓` 화살표

## 파일 시스템 탐색

### pwd (Print Working Directory)

현재 위치한 디렉토리 확인

```bash
pwd
```

출력 예시:
```
/home/pi
```

### ls (List)

디렉토리 내용 나열

```bash
# 기본 사용
ls

# 상세 정보 포함
ls -l

# 숨김 파일 포함
ls -a

# 상세 정보 + 숨김 파일
ls -la

# 사람이 읽기 쉬운 크기
ls -lh

# 특정 디렉토리 내용
ls /home/pi/Documents
```

**옵션 설명**:
- `-l`: 상세 정보 (권한, 소유자, 크기, 날짜)
- `-a`: 숨김 파일 포함 (`.`로 시작하는 파일)
- `-h`: 사람이 읽기 쉬운 형식 (KB, MB 등)
- `-t`: 수정 시간 순 정렬
- `-r`: 역순 정렬
- `-R`: 하위 디렉토리까지 재귀적으로

### cd (Change Directory)

디렉토리 이동

```bash
# 홈 디렉토리로
cd
cd ~

# 특정 디렉토리로
cd /home/pi/Documents

# 상위 디렉토리로
cd ..

# 이전 디렉토리로
cd -

# 절대 경로
cd /var/log

# 상대 경로
cd Documents/projects
```

**경로 종류**:
- **절대 경로**: `/`로 시작, 루트부터의 전체 경로
- **상대 경로**: 현재 위치 기준

**특수 디렉토리**:
- `.`: 현재 디렉토리
- `..`: 상위 디렉토리
- `~`: 홈 디렉토리
- `/`: 루트 디렉토리

## 파일 및 디렉토리 관리

### mkdir (Make Directory)

디렉토리 생성

```bash
# 단일 디렉토리
mkdir myproject

# 여러 디렉토리
mkdir dir1 dir2 dir3

# 중첩 디렉토리 (부모도 함께 생성)
mkdir -p projects/python/scripts
```

### touch

빈 파일 생성 또는 파일 수정 시간 업데이트

```bash
# 새 파일 생성
touch newfile.txt

# 여러 파일 생성
touch file1.py file2.py file3.py
```

### cp (Copy)

파일/디렉토리 복사

```bash
# 파일 복사
cp source.txt destination.txt

# 디렉토리로 복사
cp file.txt /home/pi/backup/

# 디렉토리 전체 복사 (재귀적)
cp -r sourcedir/ destdir/

# 대화형 모드 (덮어쓰기 전 확인)
cp -i file.txt backup.txt

# 상세 출력
cp -v file.txt copy.txt
```

**옵션**:
- `-r`: 디렉토리 재귀 복사
- `-i`: 대화형 모드 (덮어쓰기 전 확인)
- `-v`: 상세 출력
- `-u`: 최신 파일만 복사

### mv (Move)

파일/디렉토리 이동 또는 이름 변경

```bash
# 파일 이동
mv file.txt /home/pi/Documents/

# 파일 이름 변경
mv oldname.txt newname.txt

# 디렉토리 이동
mv mydir/ /home/pi/projects/

# 여러 파일을 디렉토리로 이동
mv file1.txt file2.txt /backup/
```

### rm (Remove)

파일/디렉토리 삭제

```bash
# 파일 삭제
rm file.txt

# 여러 파일 삭제
rm file1.txt file2.txt

# 대화형 모드
rm -i file.txt

# 디렉토리 삭제 (재귀적)
rm -r mydir/

# 강제 삭제 (확인 없이)
rm -rf mydir/
```

⚠️ **경고**:
- `rm -rf /`는 절대 실행하지 마세요! (시스템 파괴)
- 삭제된 파일은 복구 불가능
- 중요 파일 삭제 전 `-i` 옵션 사용

### rmdir

빈 디렉토리 삭제

```bash
rmdir emptydir/
```

## 파일 내용 보기 및 편집

### cat (Concatenate)

파일 내용 출력

```bash
# 파일 내용 보기
cat file.txt

# 여러 파일 연결하여 보기
cat file1.txt file2.txt

# 파일 내용을 새 파일로
cat file1.txt > newfile.txt

# 파일 내용을 기존 파일에 추가
cat file1.txt >> existing.txt

# 줄 번호 표시
cat -n file.txt
```

### less / more

파일 내용을 페이지 단위로 보기

```bash
# less (더 많은 기능, 역방향 스크롤 가능)
less file.txt

# more (단순)
more file.txt
```

**less 내부 명령어**:
- `Space`: 다음 페이지
- `b`: 이전 페이지
- `↓/↑`: 한 줄씩 이동
- `/keyword`: 검색
- `n`: 다음 검색 결과
- `q`: 종료

### head / tail

파일의 처음/끝 부분 보기

```bash
# 처음 10줄
head file.txt

# 처음 20줄
head -n 20 file.txt

# 마지막 10줄
tail file.txt

# 마지막 20줄
tail -n 20 file.txt

# 실시간 로그 모니터링
tail -f /var/log/syslog
```

### nano

간단한 텍스트 에디터

```bash
nano file.txt
```

**nano 명령어**:
- `Ctrl + O`: 저장
- `Ctrl + X`: 종료
- `Ctrl + K`: 줄 잘라내기
- `Ctrl + U`: 붙여넣기
- `Ctrl + W`: 검색
- `Ctrl + G`: 도움말

### vi / vim

강력한 텍스트 에디터

```bash
vim file.txt
```

**기본 모드**:
- **명령 모드** (기본): 커서 이동, 삭제 등
- **입력 모드**: 텍스트 입력 (`i` 키로 진입)
- **명령줄 모드**: 저장, 종료 등 (`:` 키로 진입)

**기본 명령어**:
- `i`: 입력 모드
- `Esc`: 명령 모드로 돌아가기
- `:w`: 저장
- `:q`: 종료
- `:wq` 또는 `:x`: 저장 후 종료
- `:q!`: 저장 안하고 강제 종료

## 권한 관리

### 권한 이해하기

```bash
ls -l file.txt
```

출력:
```
-rw-r--r-- 1 pi pi 1234 Nov 16 10:00 file.txt
```

**권한 구조**: `-rw-r--r--`
- 첫 번째 문자: 파일 타입
  - `-`: 일반 파일
  - `d`: 디렉토리
  - `l`: 심볼릭 링크
- 다음 9자: 권한 (3개씩 묶음)
  - `rw-`: 소유자 권한 (읽기, 쓰기)
  - `r--`: 그룹 권한 (읽기만)
  - `r--`: 기타 사용자 권한 (읽기만)

**권한 문자**:
- `r` (read): 읽기 (4)
- `w` (write): 쓰기 (2)
- `x` (execute): 실행 (1)
- `-`: 권한 없음

### chmod (Change Mode)

파일 권한 변경

```bash
# 숫자 방식
chmod 644 file.txt  # rw-r--r--
chmod 755 script.sh # rwxr-xr-x
chmod 777 file.txt  # rwxrwxrwx

# 문자 방식
chmod u+x script.sh   # 소유자에게 실행 권한 추가
chmod g-w file.txt    # 그룹의 쓰기 권한 제거
chmod o+r file.txt    # 기타 사용자에게 읽기 권한 추가
chmod a+x script.sh   # 모두에게 실행 권한 추가

# 재귀적으로 디렉토리 전체에 적용
chmod -R 755 mydir/
```

**일반적인 권한**:
- `644`: 파일 기본 (소유자 읽기/쓰기, 나머지 읽기만)
- `755`: 실행 파일, 디렉토리 (소유자 모든 권한, 나머지 읽기/실행)
- `600`: 비밀 파일 (소유자만 읽기/쓰기)
- `700`: 비밀 디렉토리 (소유자만 모든 권한)

### chown (Change Owner)

파일 소유자 변경

```bash
# 소유자 변경
sudo chown newuser file.txt

# 소유자와 그룹 변경
sudo chown newuser:newgroup file.txt

# 그룹만 변경
sudo chown :newgroup file.txt

# 재귀적으로
sudo chown -R pi:pi /home/pi/mydir/
```

## 프로세스 관리

### ps (Process Status)

실행 중인 프로세스 확인

```bash
# 현재 터미널의 프로세스
ps

# 모든 프로세스 (상세)
ps aux

# 특정 프로세스 검색
ps aux | grep python
```

### top / htop

실시간 프로세스 모니터링

```bash
# top (기본)
top

# htop (더 보기 좋음, 설치 필요)
htop
```

**top 명령어**:
- `q`: 종료
- `k`: 프로세스 종료
- `M`: 메모리 사용량 순 정렬
- `P`: CPU 사용량 순 정렬

### kill

프로세스 종료

```bash
# 프로세스 ID로 종료
kill 1234

# 강제 종료
kill -9 1234

# 프로세스 이름으로 종료
killall python3
```

### bg / fg

백그라운드/포그라운드 프로세스

```bash
# 프로그램을 백그라운드에서 실행
python script.py &

# 현재 프로세스를 백그라운드로
# (Ctrl+Z로 일시정지 후)
bg

# 백그라운드 프로세스를 포그라운드로
fg
```

## 패키지 관리

### apt (Advanced Package Tool)

소프트웨어 설치 및 관리

```bash
# 패키지 목록 업데이트
sudo apt update

# 시스템 업그레이드
sudo apt upgrade

# 전체 업그레이드
sudo apt full-upgrade

# 패키지 설치
sudo apt install package-name

# 여러 패키지 동시 설치
sudo apt install git vim htop

# 패키지 제거
sudo apt remove package-name

# 패키지와 설정 파일 제거
sudo apt purge package-name

# 불필요한 패키지 제거
sudo apt autoremove

# 패키지 검색
apt search keyword

# 패키지 정보 확인
apt show package-name
```

### dpkg

개별 패키지 관리

```bash
# 설치된 패키지 목록
dpkg -l

# 특정 패키지 검색
dpkg -l | grep python

# .deb 파일 설치
sudo dpkg -i package.deb

# 패키지 제거
sudo dpkg -r package-name
```

## 네트워크 명령어

### ping

네트워크 연결 테스트

```bash
# 호스트에 핑
ping google.com

# 4번만 핑
ping -c 4 google.com

# IP 주소로 핑
ping 8.8.8.8
```

### ifconfig / ip

네트워크 인터페이스 확인

```bash
# 네트워크 인터페이스 확인 (구버전)
ifconfig

# 네트워크 인터페이스 확인 (신버전)
ip addr show
ip a

# 특정 인터페이스만
ip addr show wlan0
```

### wget / curl

파일 다운로드

```bash
# wget
wget https://example.com/file.zip

# 다른 이름으로 저장
wget -O newname.zip https://example.com/file.zip

# curl
curl -O https://example.com/file.zip

# curl (다른 이름으로)
curl -o newname.zip https://example.com/file.zip
```

### ssh

원격 접속

```bash
# SSH 접속
ssh username@hostname

# 포트 지정
ssh -p 2222 username@hostname

# 파일 전송 (SCP)
scp file.txt username@hostname:/remote/path/
scp username@hostname:/remote/file.txt ./
```

## 시스템 정보

### uname

시스템 정보

```bash
# 커널 이름
uname

# 모든 정보
uname -a

# 커널 버전
uname -r

# 아키텍처
uname -m
```

### df

디스크 사용량

```bash
# 디스크 사용량
df

# 사람이 읽기 쉬운 형식
df -h

# 특정 파일시스템만
df -h /home
```

### du

디렉토리 크기

```bash
# 현재 디렉토리 크기
du -sh .

# 하위 디렉토리 크기
du -h --max-depth=1

# 특정 디렉토리
du -sh /home/pi/Documents
```

### free

메모리 사용량

```bash
# 메모리 정보
free

# 사람이 읽기 쉬운 형식
free -h
```

### uptime

시스템 가동 시간

```bash
uptime
```

## 유용한 팁

### 파이프 (|)

명령어 연결

```bash
# 출력을 다음 명령어의 입력으로
ls -la | less

# 프로세스 검색
ps aux | grep python

# 파일 개수 세기
ls | wc -l
```

### 리다이렉션 (>, >>)

출력을 파일로 저장

```bash
# 출력을 파일로 (덮어쓰기)
ls -la > output.txt

# 출력을 파일에 추가
echo "New line" >> output.txt

# 에러도 파일로
command 2> error.log

# 모든 출력을 파일로
command > output.log 2>&1
```

### 명령어 히스토리

```bash
# 명령어 히스토리 보기
history

# 특정 명령어 재실행
!123  # 123번째 명령어 실행

# 마지막 명령어 재실행
!!

# 검색하여 실행
Ctrl + R (역방향 검색)
```

### alias

명령어 단축

```bash
# 임시 alias
alias ll='ls -la'
alias update='sudo apt update && sudo apt upgrade'

# 영구 alias (~/.bashrc에 추가)
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
```

### grep

텍스트 검색

```bash
# 파일에서 검색
grep "keyword" file.txt

# 대소문자 무시
grep -i "keyword" file.txt

# 재귀 검색 (디렉토리 내 모든 파일)
grep -r "keyword" /path/to/dir/

# 줄 번호 표시
grep -n "keyword" file.txt

# 매칭되지 않는 줄
grep -v "keyword" file.txt
```

### find

파일 찾기

```bash
# 이름으로 검색
find /home/pi -name "*.txt"

# 타입으로 검색
find /home/pi -type f  # 파일만
find /home/pi -type d  # 디렉토리만

# 크기로 검색
find /home/pi -size +10M  # 10MB 이상

# 수정 시간으로 검색
find /home/pi -mtime -7   # 최근 7일 이내
```

### tar

압축 및 압축 해제

```bash
# 압축 (생성)
tar -czf archive.tar.gz /path/to/dir/

# 압축 해제
tar -xzf archive.tar.gz

# 압축 내용 보기
tar -tzf archive.tar.gz
```

**옵션**:
- `c`: 생성 (create)
- `x`: 압축 해제 (extract)
- `z`: gzip 압축
- `f`: 파일 이름 지정
- `v`: 상세 출력 (verbose)
- `t`: 내용 보기 (list)

## 실습 예제

### 예제 1: 프로젝트 디렉토리 만들기

```bash
# 홈 디렉토리로 이동
cd ~

# 프로젝트 디렉토리 구조 생성
mkdir -p projects/python/scripts
mkdir -p projects/web/html
mkdir -p projects/backup

# 확인
tree projects  # 또는 ls -R projects
```

### 예제 2: 시스템 정보 파일 생성

```bash
# 시스템 정보 수집
echo "=== System Information ===" > sysinfo.txt
uname -a >> sysinfo.txt
echo "" >> sysinfo.txt
echo "=== Disk Usage ===" >> sysinfo.txt
df -h >> sysinfo.txt
echo "" >> sysinfo.txt
echo "=== Memory ===" >> sysinfo.txt
free -h >> sysinfo.txt

# 확인
cat sysinfo.txt
```

### 예제 3: 로그 모니터링

```bash
# 실시간 시스템 로그 보기
tail -f /var/log/syslog

# 특정 키워드만
tail -f /var/log/syslog | grep error
```

## 다음 단계

리눅스 기본 명령어를 배웠습니다! 이제 원격 접속 방법을 알아봅시다.

➡️ [다음: 원격 접속](remote-access.md)

## 참고 자료

- [Linux 명령어 치트시트](https://www.linuxtrainingacademy.com/linux-commands-cheat-sheet/)
- [Bash 가이드](https://mywiki.wooledge.org/BashGuide)
- [리눅스 파일 시스템 계층 구조](https://www.pathname.com/fhs/)
