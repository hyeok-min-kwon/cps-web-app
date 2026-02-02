#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/ml_model"

echo "================================================"
echo "Python API 서버 시작 중..."
echo "================================================"

# venv 확인
if [ ! -d "venv" ]; then
    echo "✗ Python 가상환경이 없습니다."
    echo ""
    echo "다음 명령어로 환경을 생성하세요:"
    echo "  cd ml_model"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "✓ Python 가상환경 찾음"

# venv 활성화
source venv/bin/activate

# Python 버전 확인
echo "✓ Python 버전: $(python --version)"
echo ""

# 모델 파일 존재 확인
if [ ! -d "models" ] || [ ! -f "models/failure_model.pkl" ]; then
    echo ""
    echo "⚠️  학습된 모델이 없습니다!"
    echo "다음 명령어로 모델을 먼저 학습시키세요:"
    echo "  cd ml_model"
    echo "  source venv/bin/activate"
    echo "  python train_model.py"
    echo ""
    exit 1
fi

echo "✓ 모델 파일 확인됨"

# API 서버 실행
echo ""
echo "✓ API 서버를 http://localhost:8000 에서 실행합니다."
echo "✓ API 문서: http://localhost:8000/docs"
echo ""
echo "중지하려면 Ctrl+C를 누르세요."
echo ""

python -m uvicorn api_server:app --reload --port 8000 --host 0.0.0.0
