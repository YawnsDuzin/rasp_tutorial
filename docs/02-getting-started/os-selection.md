# 03. OS 선택 가이드

라즈베리파이에 설치할 수 있는 다양한 운영체제(OS)를 소개하고, 용도에 맞는 OS를 선택하는 방법을 안내합니다.

## 라즈베리파이용 운영체제 개요

라즈베리파이는 ARM 아키텍처를 사용하므로, ARM용으로 컴파일된 운영체제만 설치할 수 있습니다. 다행히 다양한 리눅스 배포판과 특수 목적 OS들이 라즈베리파이를 지원합니다.

## 1. Raspberry Pi OS (추천)

### 개요
- **기반**: Debian Linux
- **개발**: 라즈베리파이 재단 공식 OS
- **추천 대상**: 모든 사용자 (특히 초보자)

### 버전

#### Raspberry Pi OS (with Desktop)
- **특징**: GUI 데스크톱 환경 포함
- **크기**: 약 1.1GB
- **포함 소프트웨어**:
  - Chromium 웹 브라우저
  - LibreOffice (오피스)
  - Thonny (Python IDE)
  - Scratch (프로그래밍 학습)
  - 미디어 플레이어 등
- **용도**: 데스크톱 컴퓨터로 사용, 학습용

#### Raspberry Pi OS (with Desktop and recommended software)
- **특징**: 추가 소프트웨어 사전 설치
- **크기**: 약 2.7GB
- **추가 소프트웨어**: 교육용 앱, 프로그래밍 도구 등
- **용도**: 교육, 올인원 데스크톱

#### Raspberry Pi OS Lite
- **특징**: GUI 없는 커맨드라인 전용
- **크기**: 약 400MB
- **용도**: 서버, 헤드리스 프로젝트, IoT
- **장점**: 가볍고 빠름, 리소스 절약

### 장점
✅ 라즈베리파이에 최적화
✅ 공식 지원 및 정기 업데이트
✅ 풍부한 문서와 커뮤니티
✅ 사전 설치된 유용한 도구들
✅ 초보자 친화적

### 단점
❌ 다른 리눅스 배포판 대비 다소 보수적

### 추천 사용 사례
- 라즈베리파이 입문
- 프로그래밍 학습
- GPIO 프로젝트
- 데스크톱 컴퓨터
- 홈 서버

## 2. Ubuntu

### 개요
- **기반**: Debian (Raspberry Pi OS와 유사)
- **개발**: Canonical
- **추천 대상**: 우분투에 익숙한 사용자, 서버 운영자

### 버전

#### Ubuntu Desktop
- GUI 데스크톱 환경
- GNOME 데스크톱
- Pi 4/5 (4GB 이상 RAM) 권장

#### Ubuntu Server
- GUI 없는 서버용
- 가볍고 안정적
- 2GB RAM으로도 충분

#### Ubuntu Core
- IoT 전용 경량 OS
- Snap 패키지 기반
- 보안과 업데이트에 중점

### 장점
✅ 익숙한 우분투 환경
✅ 풍부한 패키지 저장소
✅ 서버 운영에 적합
✅ LTS(장기 지원) 버전 제공
✅ 클라우드/DevOps 도구 지원

### 단점
❌ Raspberry Pi OS보다 무거움
❌ 라즈베리파이 특화 도구 부족

### 추천 사용 사례
- 웹 서버
- 데이터베이스 서버
- 개발 환경
- Kubernetes/Docker 실습

## 3. RetroPie

### 개요
- **기반**: Raspberry Pi OS
- **목적**: 레트로 게임 에뮬레이션
- **추천 대상**: 고전 게임 팬

### 특징
- EmulationStation 프론트엔드
- 다양한 게임기 에뮬레이터 포함:
  - NES, SNES, Genesis
  - PlayStation, N64
  - 아케이드 (MAME)
  - 등 50개 이상
- 게임패드 지원
- 스크랩핑 (게임 정보/이미지 다운로드)

### 장점
✅ 설정이 간편
✅ 통합된 게임 라이브러리
✅ 활발한 커뮤니티

### 단점
❌ 게임 ROM은 별도로 준비 필요
❌ 저작권 문제 주의

### 추천 사용 사례
- 레트로 게임 콘솔
- 아케이드 머신
- 게임 바

## 4. LibreELEC / OSMC

### 개요
- **목적**: 미디어 센터
- **기반**: Kodi 미디어 플레이어
- **추천 대상**: 홈 시어터 구축

### LibreELEC
- Kodi에만 집중한 경량 OS
- 빠른 부팅
- 자동 업데이트

### OSMC (Open Source Media Center)
- Kodi + Debian 기반
- 더 많은 커스터마이징 가능
- 앱 스토어 포함

### 장점
✅ 미디어 재생에 최적화
✅ 직관적인 인터페이스
✅ 다양한 포맷 지원
✅ 리모컨 지원

### 추천 사용 사례
- 홈 시어터 PC
- 미디어 스트리밍
- 넷플릭스, 유튜브 등

## 5. Pi-hole OS

### 개요
- **목적**: 네트워크 광고 차단기
- **기반**: Raspberry Pi OS Lite
- **추천 대상**: 네트워크 관리자

### 특징
- DNS 수준에서 광고 차단
- 전체 네트워크에 적용
- 웹 인터페이스로 관리
- 통계 및 분석 기능

### 장점
✅ 모든 기기에서 광고 차단
✅ 네트워크 속도 향상
✅ 프라이버시 보호

### 추천 사용 사례
- 홈 네트워크 광고 차단
- DNS 서버
- 네트워크 모니터링

## 6. Kali Linux

### 개요
- **목적**: 보안 테스팅
- **기반**: Debian
- **추천 대상**: 보안 전문가, 학습자

### 특징
- 침투 테스팅 도구 사전 설치
- 600개 이상의 보안 도구
- 무선 네트워크 분석
- 취약점 스캔

### 장점
✅ 포괄적인 보안 도구
✅ 정기적인 업데이트
✅ 풍부한 문서

### 단점
❌ 초보자에게 어려움
❌ 법적/윤리적 책임 필요

### 추천 사용 사례
- 보안 학습
- 침투 테스팅 (승인된 환경)
- 네트워크 보안 분석

## 7. Windows 10/11 IoT Core

### 개요
- **개발**: Microsoft
- **목적**: IoT 장치 개발
- **추천 대상**: .NET 개발자

### 특징
- UWP 앱 실행
- Visual Studio 통합
- Azure IoT 연동

### 장점
✅ Windows 개발 도구 활용
✅ .NET/C# 지원

### 단점
❌ 제한적인 기능 (GUI 없음)
❌ Pi 2/3만 공식 지원

### 추천 사용 사례
- IoT 프로토타이핑
- .NET 기반 프로젝트

## OS 선택 가이드

### 용도별 추천

| 용도 | 추천 OS | 이유 |
|------|---------|------|
| **입문/학습** | Raspberry Pi OS (Desktop) | 사용하기 쉽고 문서가 풍부 |
| **프로그래밍** | Raspberry Pi OS (Desktop) | 개발 도구 사전 설치 |
| **서버** | Raspberry Pi OS Lite 또는 Ubuntu Server | 가볍고 안정적 |
| **IoT** | Raspberry Pi OS Lite | 최적화되고 가벼움 |
| **미디어 센터** | LibreELEC 또는 OSMC | Kodi에 최적화 |
| **게임** | RetroPie | 에뮬레이터 올인원 |
| **보안 학습** | Kali Linux | 보안 도구 포함 |
| **데스크톱** | Raspberry Pi OS 또는 Ubuntu | 완전한 PC 경험 |

### 모델별 추천

| 모델 | 추천 OS |
|------|---------|
| **Pi Zero/Zero W** | Raspberry Pi OS Lite (리소스 제약) |
| **Pi Zero 2 W** | Raspberry Pi OS Lite 또는 Desktop |
| **Pi 3** | Raspberry Pi OS, Ubuntu Server |
| **Pi 4 (2GB)** | Raspberry Pi OS, Ubuntu Server |
| **Pi 4 (4GB+)** | 모든 OS (Ubuntu Desktop 포함) |
| **Pi 5** | 모든 OS (최고 성능) |

### 경험 수준별 추천

| 경험 | 추천 OS |
|------|---------|
| **초보자** | Raspberry Pi OS (Desktop) |
| **리눅스 경험자** | Ubuntu, Raspberry Pi OS Lite |
| **고급 사용자** | 용도에 맞는 특화 OS |

## 결정 플로우차트

```
라즈베리파이 처음 사용?
├─ 예 → Raspberry Pi OS (Desktop)
└─ 아니오
   ├─ 데스크톱으로 사용?
   │  ├─ 예 → Raspberry Pi OS / Ubuntu Desktop
   │  └─ 아니오
   │     ├─ 서버로 사용?
   │     │  ├─ 예 → Raspberry Pi OS Lite / Ubuntu Server
   │     │  └─ 아니오
   │     │     ├─ 미디어 센터?
   │     │     │  └─ 예 → LibreELEC / OSMC
   │     │     ├─ 게임 에뮬레이션?
   │     │     │  └─ 예 → RetroPie
   │     │     └─ 특수 목적
   │     │        └─ 용도에 맞는 특화 OS
```

## 다중 부팅

하나의 라즈베리파이에서 여러 OS를 사용하고 싶다면:

### NOOBS (New Out Of Box Software)
- 여러 OS 설치 가능
- 부팅 시 OS 선택
- 초보자 친화적
- ⚠️ 2020년 이후 업데이트 중단

### 대안: 여러 SD 카드
- 각 SD 카드에 다른 OS 설치
- SD 카드 교체로 OS 전환
- 간단하고 안전

## 다음 단계

OS를 선택했다면, 이제 설치를 시작합니다!

**대부분의 사용자에게 추천**: Raspberry Pi OS (Desktop)

➡️ [다음: OS 설치하기](os-installation.md)

## 참고 자료

- [Raspberry Pi OS 다운로드](https://www.raspberrypi.com/software/operating-systems/)
- [Ubuntu for Raspberry Pi](https://ubuntu.com/download/raspberry-pi)
- [RetroPie](https://retropie.org.uk/)
- [LibreELEC](https://libreelec.tv/)
- [OSMC](https://osmc.tv/)
- [라즈베리파이 OS 비교](https://www.raspberrypi.com/software/)
