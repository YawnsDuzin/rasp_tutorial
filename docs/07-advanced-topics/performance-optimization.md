# 15. 성능 최적화

라즈베리파이의 성능을 최대한 끌어올리는 방법을 배웁니다.

## 시스템 모니터링

### CPU 및 메모리 사용량

```bash
# 실시간 모니터링
htop

# CPU 정보
lscpu

# 메모리 정보
free -h

# 온도 확인
vcgencmd measure_temp

# CPU 클럭 속도
vcgencmd measure_clock arm

# 전압 확인
vcgencmd measure_volts
```

### 온도 모니터링 스크립트

```python
# temp_monitor.py
import subprocess
import time

def get_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'],
                          capture_output=True, text=True)
    temp_str = result.stdout.strip()
    # "temp=42.8'C" 형식
    temp = float(temp_str.split('=')[1].split("'")[0])
    return temp

def get_cpu_usage():
    with open('/proc/stat', 'r') as f:
        line = f.readline()
    cpu_times = [int(x) for x in line.split()[1:]]
    idle_time = cpu_times[3]
    total_time = sum(cpu_times)
    return 100 * (1 - idle_time / total_time)

while True:
    temp = get_temperature()
    print(f"온도: {temp}°C", end="")

    if temp > 75:
        print(" ⚠️ 과열!")
    elif temp > 60:
        print(" ⚡ 높음")
    else:
        print(" ✓ 정상")

    time.sleep(2)
```

## 냉각 시스템

### 쿨링 팬 자동 제어

```python
# fan_control.py
import subprocess
import time
from gpiozero import OutputDevice

FAN_PIN = 18
TEMP_THRESHOLD = 60  # 60°C 이상에서 팬 가동

fan = OutputDevice(FAN_PIN)

def get_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'],
                          capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp = float(temp_str.split('=')[1].split("'")[0])
    return temp

try:
    while True:
        temp = get_temperature()
        print(f"온도: {temp}°C", end=" ")

        if temp >= TEMP_THRESHOLD:
            fan.on()
            print("팬 ON")
        else:
            fan.off()
            print("팬 OFF")

        time.sleep(5)

except KeyboardInterrupt:
    fan.off()
    print("\n종료")
```

## 오버클러킹

⚠️ **주의**: 오버클러킹은 보증이 무효화될 수 있으며, 적절한 냉각이 필요합니다.

### 설정

```bash
sudo nano /boot/config.txt
```

**Raspberry Pi 4 예시**:
```ini
# 중간 오버클러킹
over_voltage=2
arm_freq=1750

# 강력한 오버클러킹 (냉각 필수!)
over_voltage=6
arm_freq=2000
```

**재부팅**:
```bash
sudo reboot
```

### 안정성 테스트

```bash
# CPU 스트레스 테스트
sudo apt install stress
stress --cpu 4 --timeout 300s

# 온도 모니터링과 함께
watch -n 1 vcgencmd measure_temp
```

## 메모리 최적화

### GPU 메모리 조절

```bash
sudo raspi-config
# Performance Options → GPU Memory
```

- **Desktop 사용**: 128MB~256MB
- **Headless/서버**: 16MB~64MB

### Swap 파일 조정

```bash
# Swap 크기 변경
sudo nano /etc/dphys-swapfile
```

```
# 변경 (MB 단위)
CONF_SWAPSIZE=2048
```

```bash
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### 불필요한 서비스 비활성화

```bash
# 실행 중인 서비스 확인
systemctl list-units --type=service --state=running

# 불필요한 서비스 비활성화
sudo systemctl disable bluetooth
sudo systemctl disable cups
sudo systemctl disable avahi-daemon
```

## 디스크 I/O 최적화

### SD 카드 성능 테스트

```bash
# 쓰기 속도
dd if=/dev/zero of=~/test.tmp bs=500K count=1024
# 읽기 속도
dd if=~/test.tmp of=/dev/null bs=500K count=1024
rm ~/test.tmp
```

### 로그 파일을 RAM에 저장

```bash
sudo nano /etc/fstab
```

**추가**:
```
tmpfs /tmp tmpfs defaults,noatime,nosuid,size=100m 0 0
tmpfs /var/tmp tmpfs defaults,noatime,nosuid,size=30m 0 0
tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0
```

### USB 부팅 (더 빠른 SSD 사용)

Pi 4/5에서 USB SSD로 부팅하면 성능 향상:

```bash
# EEPROM 업데이트
sudo apt update
sudo apt full-upgrade
sudo rpi-eeprom-update -d -a

# USB 부팅 활성화
sudo raspi-config
# Advanced Options → Boot Order → USB Boot
```

## 네트워크 최적화

### 고정 IP로 빠른 연결

```bash
sudo nano /etc/dhcpcd.conf
```

```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

### DNS 캐싱

```bash
sudo apt install dnsmasq

sudo nano /etc/dnsmasq.conf
```

```
cache-size=1000
```

## Python 성능 최적화

### PyPy 사용

PyPy는 JIT 컴파일러로 Python 코드를 더 빠르게 실행:

```bash
sudo apt install pypy3
pypy3 your_script.py
```

### NumPy 최적화

```bash
# OpenBLAS 사용
sudo apt install libopenblas-dev
pip3 install numpy --no-binary numpy
```

## 전력 관리

### 전력 소비 측정

```bash
vcgencmd get_throttled
```

**출력 해석**:
- `0x0`: 정상
- `0x50000`: Under-voltage 감지
- `0x50005`: Under-voltage + Throttling

### 전력 절약 모드

```bash
# Wi-Fi 절전 모드 비활성화 (안정성 향상)
sudo iwconfig wlan0 power off

# CPU 거버너 설정
sudo apt install cpufrequtils

# Performance 모드 (최대 성능)
sudo cpufreq-set -g performance

# Powersave 모드 (절전)
sudo cpufreq-set -g powersave
```

## 벤치마크

### sysbench

```bash
sudo apt install sysbench

# CPU 테스트
sysbench cpu --threads=4 run

# 메모리 테스트
sysbench memory run

# 파일 I/O 테스트
sysbench fileio --file-test-mode=seqwr run
```

## 최적화 체크리스트

### 성능 향상을 위한 단계

- [ ] 불필요한 서비스 비활성화
- [ ] GPU 메모리 조정 (용도에 맞게)
- [ ] Swap 크기 최적화
- [ ] 로그 파일 RAM 저장 (선택)
- [ ] 냉각 시스템 설치
- [ ] 고정 IP 사용
- [ ] USB SSD 부팅 (Pi 4/5)
- [ ] 적절한 전원 어댑터 사용

## 다음 단계

➡️ [다음: 보안](security.md)

## 참고 자료

- [라즈베리파이 오버클러킹 가이드](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking)
- [성능 최적화 팁](https://www.raspberrypi.com/documentation/computers/configuration.html)
