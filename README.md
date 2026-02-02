# 🏭 CPS 고장 예측 시스템 (Predictive Maintenance System)

실시간 센서 데이터를 기반으로 기계 고장을 예측하는 AI 기반 웹 애플리케이션입니다.

[![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-F7931E?logo=scikitlearn)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [시스템 아키텍처](#-시스템-아키텍처)
- [데이터셋](#-데이터셋)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [모델 성능](#-모델-성능)
- [프로젝트 구조](#-프로젝트-구조)
- [API 문서](#-api-문서)
- [문제 해결](#-문제-해결)

## 🎯 프로젝트 소개

이 프로젝트는 **예방 정비(Predictive Maintenance)**를 위한 AI 시스템으로, 산업 현장의 센서 데이터를 실시간으로 분석하여 기계 고장을 사전에 예측합니다. 머신러닝 모델을 통해 고장 발생 확률과 고장 타입을 예측하여, 계획되지 않은 다운타임을 줄이고 유지보수 비용을 절감할 수 있습니다.

### 💡 왜 예방 정비가 중요한가요?

- **비용 절감**: 계획되지 않은 고장으로 인한 생산 중단 방지
- **효율성 향상**: 필요한 시점에만 정비를 수행하여 자원 최적화
- **안전성 강화**: 위험한 고장 상황을 사전에 예측하고 대응

## ✨ 주요 기능

### 1. 실시간 고장 예측
- 6가지 센서 데이터 입력 (온도, 회전속도, 토크 등)
- 기계 고장 발생 확률 예측 (0-100%)
- 정상/고장 상태 분류

### 2. 고장 타입 분석
5가지 고장 유형별 발생 확률 제공:
- **TWF** (Tool Wear Failure): 공구 마모 고장
- **HDF** (Heat Dissipation Failure): 열 방출 고장
- **PWF** (Power Failure): 전력 고장
- **OSF** (Overstrain Failure): 과부하 고장
- **RNF** (Random Failure): 랜덤 고장

### 3. 직관적인 웹 UI
- 슬라이더를 통한 쉬운 센서 값 조정
- 실시간 결과 시각화
- 고장 타입별 확률 차트

### 4. RESTful API
- FastAPI 기반 고성능 API
- Swagger UI를 통한 API 문서 자동 생성
- JSON 형식의 간편한 데이터 교환

## 🛠️ 기술 스택

### Backend (ML API)
- **Python 3.10+**: 머신러닝 모델 개발 (3.10-3.12 호환)
- **FastAPI 0.104.1**: 고성능 비동기 웹 프레임워크
- **scikit-learn 1.3.2**: 머신러닝 모델 학습 및 예측
- **pandas 2.1.3**: 데이터 전처리
- **uvicorn 0.24.0**: ASGI 서버

### Frontend & Web Server
- **ASP.NET Core 10.0**: 웹 애플리케이션 프레임워크
- **Razor Pages**: 서버 사이드 렌더링
- **Bootstrap 5**: 반응형 UI 디자인
- **C# 10**: 백엔드 로직

### ML Models
- **Random Forest Classifier**: 고장 여부 예측
- **MultiOutput Classifier**: 고장 타입 예측
- **Standard Scaler**: 특성 정규화

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                       사용자                              │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Request
                        ▼
┌─────────────────────────────────────────────────────────┐
│          ASP.NET Core Web Application (C#)              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Razor Pages (UI)                                 │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                  │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  PredictionService (API Client)                   │  │
│  └───────────────────┬───────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                        │ HTTP POST /predict
                        ▼
┌─────────────────────────────────────────────────────────┐
│            FastAPI Server (Python)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Prediction Endpoint                              │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                  │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  ML Models                                        │  │
│  │  - Random Forest (Failure Detection)              │  │
│  │  - MultiOutput Classifier (Failure Types)         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📊 데이터셋

### 데이터 구성
- **총 샘플 수**: 10,000개
- **정상 데이터**: 9,661개 (96.6%)
- **고장 데이터**: 339개 (3.4%)

### 입력 특성 (6개)
| 특성 | 설명 | 범위 | 단위 |
|------|------|------|------|
| Type | 제품 품질 타입 | L, M, H | - |
| Air temperature | 공기 온도 | 290-310 | K |
| Process temperature | 공정 온도 | 300-315 | K |
| Rotational speed | 회전 속도 | 1000-3000 | rpm |
| Torque | 토크 | 0-100 | Nm |
| Tool wear | 공구 마모 시간 | 0-300 | min |

### 출력 레이블
- **Machine failure**: 고장 여부 (0: 정상, 1: 고장)
- **TWF, HDF, PWF, OSF, RNF**: 각 고장 타입 발생 여부

## ⚡ 빠른 시작 (Quick Start)

```bash
# 1. 저장소 클론
git clone https://github.com/Hyeok-Min-Kwon/CPS-Web-App
cd CPSwithML

# 2. Python 가상환경 설정 및 패키지 설치
cd ml_model
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 모델 학습 (이미 학습된 모델이 있다면 생략 가능)
python train_model.py
cd ..

# 4. 실행 권한 부여 (macOS/Linux)
chmod +x start_api.sh start_web.sh

# 5. API 서버 실행 (새 터미널 창)
./start_api.sh

# 6. 웹 앱 실행 (다른 터미널 창)
./start_web.sh

# 7. 브라우저에서 접속
# http://localhost:5214
```

## 🚀 상세 설치 방법

### 사전 요구사항
- [.NET SDK 10.0+](https://dotnet.microsoft.com/download)
- Python 3.10+ (Homebrew, Anaconda, 또는 공식 Python 설치)
- Git

### 1. 저장소 클론
```bash
git clone https://github.com/Hyeok-Min-Kwon/CPS-Web-App
cd CPSwithML
```

### 2. Python 환경 설정

#### 옵션 A: venv 사용 (추천)
Python 내장 가상환경을 사용합니다. conda 설치 불필요.

```bash
cd ml_model
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **참고**: `venv` 디렉토리는 `.gitignore`에 포함되어 있어 Git에 추적되지 않습니다.

#### 옵션 B: conda 사용
Anaconda/Miniconda가 설치되어 있는 경우.

```bash
conda create -n cps_ml python=3.10 -y
conda activate cps_ml
pip install -r ml_model/requirements.txt
```

### 3. 머신러닝 모델 학습
```bash
cd ml_model
# venv 사용 시: source venv/bin/activate
# conda 사용 시: conda activate cps_ml
python train_model.py
```

학습이 완료되면 `ml_model/models/` 디렉토리에 다음 파일들이 생성됩니다:
- `failure_model.pkl`: 고장 여부 예측 모델
- `failure_type_model.pkl`: 고장 타입 예측 모델
- `scaler.pkl`: 특성 스케일러
- `feature_names.pkl`: 특성명 리스트

> **참고**: 모델 파일(`*.pkl`)도 `.gitignore`에 포함되어 Git에 추적되지 않습니다.

### 4. 실행 권한 부여 (Unix/Linux/macOS)
```bash
cd ..  # 프로젝트 루트로 이동
chmod +x start_api.sh start_web.sh
```

## 💻 사용 방법

### 방법 1: 실행 스크립트 사용 (추천)

#### 1단계: Python API 서버 시작
새 터미널 창을 열고:
```bash
./start_api.sh
```

다음과 같은 메시지가 나타나면 성공:
```
✓ API 서버를 http://localhost:8000 에서 실행합니다.
✓ API 문서: http://localhost:8000/docs
```

#### 2단계: C# 웹 애플리케이션 시작
**새로운 터미널 창**을 열고:
```bash
./start_web.sh
```

출력된 URL (예: http://localhost:5214)을 확인합니다.

#### 3단계: 브라우저 접속
출력된 URL로 브라우저에서 접속합니다.

### 방법 2: 수동 실행

#### Python API 서버

**venv 사용 시:**
```bash
cd ml_model
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn api_server:app --reload --port 8000
```

**conda 사용 시:**
```bash
conda activate cps_ml
cd ml_model
python -m uvicorn api_server:app --reload --port 8000
```

#### C# 웹 애플리케이션
```bash
cd CPSwithML
dotnet run
```

### 서버 중지 방법

#### 방법 1: 터미널에서 직접 중지
각 서버가 실행 중인 터미널 창에서 `Ctrl+C`를 누릅니다.

#### 방법 2: 포트로 프로세스 종료
```bash
# Python API 서버 중지 (포트 8000)
lsof -ti :8000 | xargs kill -9

# C# 웹 애플리케이션 중지 (포트 5214)
lsof -ti :5214 | xargs kill -9

# 두 서버 동시 중지
lsof -ti :8000 | xargs kill -9 && lsof -ti :5214 | xargs kill -9
```

## 📈 모델 성능

### Machine Failure 예측 모델
- **알고리즘**: Random Forest Classifier
- **정확도**: 97.6%
- **Precision (고장)**: 0.66
- **Recall (고장)**: 0.60
- **F1-Score (고장)**: 0.63

### 특성 중요도
| 순위 | 특성 | 중요도 |
|------|------|--------|
| 1 | Rotational speed | 31.6% |
| 2 | Torque | 29.6% |
| 3 | Tool wear | 20.1% |
| 4 | Air temperature | 9.8% |
| 5 | Process temperature | 6.9% |

### Failure Type 예측 모델
- **알고리즘**: MultiOutput Random Forest
- **평균 정확도**: 94-100% (타입별 상이)
- **TWF 정확도**: 94.1%
- **HDF 정확도**: 97.1%
- **PWF 정확도**: 97.1%
- **OSF 정확도**: 97.1%
- **RNF 정확도**: 100%

## 📁 프로젝트 구조

```
CPSwithML/
├── README.md                      # 프로젝트 문서
├── LICENSE                        # MIT 라이선스
├── .gitignore                     # Git 제외 파일 설정
├── start_api.sh                   # Python API 실행 스크립트 (venv 사용)
├── start_web.sh                   # C# 웹 앱 실행 스크립트
│
├── ml_model/                      # Python ML 프로젝트
│   ├── train_model.py            # 모델 학습 스크립트
│   ├── api_server.py             # FastAPI 서버
│   ├── requirements.txt          # Python 의존성
│   ├── venv/                     # Python 가상환경 (gitignore됨)
│   └── models/                   # 학습된 모델 (gitignore됨)
│       ├── failure_model.pkl
│       ├── failure_type_model.pkl
│       ├── scaler.pkl
│       └── feature_names.pkl
│
└── CPSwithML/                     # C# ASP.NET 프로젝트
    ├── Program.cs                # 애플리케이션 진입점
    ├── appsettings.json          # 설정 파일
    │
    ├── Pages/                    # Razor Pages
    │   ├── Index.cshtml          # 메인 UI
    │   ├── Index.cshtml.cs       # 페이지 모델
    │   └── Shared/               # 공유 레이아웃
    │
    ├── Services/                 # 비즈니스 로직
    │   └── PredictionService.cs  # Python API 클라이언트
    │
    ├── Models/                   # 데이터 모델
    │   ├── SensorDataDto.cs      # 센서 데이터 DTO
    │   └── PredictionResultDto.cs # 예측 결과 DTO
    │
    ├── wwwroot/                  # 정적 파일
    │   ├── css/
    │   │   │   └── prediction.css    # 커스텀 스타일
    │   └── js/
    │
    └── cps_data.csv              # 학습 데이터셋
```

## 📖 API 문서

### 엔드포인트

#### GET `/health`
API 서버 상태 확인

**응답 예시:**
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

#### POST `/predict`
센서 데이터 기반 고장 예측

**요청 본문:**
```json
{
  "type": "M",
  "air_temperature": 298.5,
  "process_temperature": 308.7,
  "rotational_speed": 1500,
  "torque": 45.0,
  "tool_wear": 50
}
```

**응답 예시:**
```json
{
  "machine_failure": {
    "prediction": 0,
    "probability": 0.0008
  },
  "failure_types": {
    "TWF": 0.00014,
    "HDF": 0.0,
    "PWF": 0.00045,
    "OSF": 0.000008,
    "RNF": 0.0
  }
}
```

### Swagger UI
API 서버 실행 후 http://localhost:8000/docs 에서 인터랙티브 API 문서를 확인할 수 있습니다.

## 🔧 문제 해결

### 1. Python 가상환경 오류

**증상**: `No module named 'uvicorn'` 또는 패키지를 찾을 수 없다는 오류

**해결 방법 (venv 사용 시):**
```bash
cd ml_model
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**해결 방법 (conda 사용 시):**
```bash
# conda 초기화 (최초 1회)
conda init zsh  # 또는 conda init bash
source ~/.zshrc  # 또는 source ~/.bashrc

# 환경 생성 및 패키지 설치
conda create -n cps_ml python=3.10 -y
conda activate cps_ml
pip install -r ml_model/requirements.txt
```

### 2. 모델 파일이 없다는 오류

**증상**: `FileNotFoundError: models/failure_model.pkl`

**해결 방법:**
```bash
cd ml_model
source venv/bin/activate  # 또는 conda activate cps_ml
python train_model.py
```

모델 학습에는 약 10-30초가 소요됩니다.

### 3. 포트가 이미 사용 중인 경우

**증상**: `ERROR: [Errno 48] Address already in use`

**해결 방법:**
```bash
# 포트 8000 사용 프로세스 확인 및 종료
lsof -ti :8000 | xargs kill -9

# 포트 5214 사용 프로세스 확인 및 종료
lsof -ti :5214 | xargs kill -9

# 현재 사용 중인 프로세스 확인
lsof -i :8000
lsof -i :5214
```

### 4. .NET SDK가 없는 경우

**증상**: `command not found: dotnet`

**해결 방법:**
- https://dotnet.microsoft.com/download 에서 .NET 10.0 SDK 다운로드 및 설치
- 설치 후 터미널 재시작
- 확인: `dotnet --version`

### 5. Python API 서버 연결 실패

**증상**: C# 앱에서 "Failed to connect to Python API"

**해결 방법:**
```bash
# API 서버 상태 확인
curl http://localhost:8000/health

# 정상 응답: {"status":"healthy","models_loaded":true}
```

체크리스트:
- [ ] Python API 서버가 실행 중인가? (터미널 1)
- [ ] 포트 8000이 열려 있는가?
- [ ] 방화벽이 로컬호스트 연결을 차단하지 않는가?
- [ ] `appsettings.json`의 `PredictionApi:BaseUrl`이 `http://localhost:8000`인가?

### 6. 권한 오류 (macOS/Linux)

**증상**: `Permission denied` when running `.sh` scripts

**해결 방법:**
```bash
chmod +x start_api.sh start_web.sh
```

### 7. Python 버전 문제

**증상**: 패키지 설치 중 호환성 오류

**해결 방법:**
- Python 3.10 이상 사용 권장
- 버전 확인: `python3 --version`
- 필요시 Python 재설치 또는 pyenv 사용

## 🤝 기여하기

기여는 언제나 환영합니다! 다음 절차를 따라주세요:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 👨‍💻 개발자

- [GitHub](https://github.com/Hyeok-Min-Kwon)

## 🙏 감사의 말

- [Predictive Maintenance Dataset (AI4I 2020)](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020) - 데이터셋 제공
- [FastAPI](https://fastapi.tiangolo.com/) - API 프레임워크
- [scikit-learn](https://scikit-learn.org/) - 머신러닝 라이브러리

## 💡 추가 정보

### 환경 변수
이 프로젝트는 기본적으로 환경 변수가 필요하지 않지만, API URL을 변경하려면 `CPSwithML/appsettings.json`을 수정하세요.

### 성능 최적화
- 프로덕션 환경에서는 `--reload` 옵션을 제거하세요
- Gunicorn + Uvicorn 조합 사용 권장
- 모델 로딩을 캐싱하여 응답 시간 단축

### 보안 고려사항
- 프로덕션 배포 시 HTTPS 사용
- CORS 설정 재검토 필요
- API 인증/권한 부여 추가 고려

### 향후 개선 사항
- [ ] 실시간 센서 데이터 스트리밍
- [ ] 모델 버전 관리 시스템
- [ ] 예측 결과 히스토리 저장
- [ ] 대시보드 및 분석 차트 추가
- [ ] Docker 컨테이너화

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
