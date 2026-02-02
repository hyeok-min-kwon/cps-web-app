#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/CPSwithML"

echo "================================================"
echo "C# 웹 애플리케이션 시작 중..."
echo "================================================"

# .NET SDK 확인
if ! command -v dotnet &> /dev/null; then
    echo "✗ .NET SDK가 설치되어 있지 않습니다."
    echo ""
    echo "다음 링크에서 .NET SDK를 다운로드하세요:"
    echo "https://dotnet.microsoft.com/download"
    exit 1
fi

echo "✓ .NET SDK 버전: $(dotnet --version)"
echo ""

# Python API 서버 확인
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  Python API 서버가 실행되지 않았습니다!"
    echo ""
    echo "다른 터미널에서 먼저 API 서버를 실행하세요:"
    echo "  ./start_api.sh"
    echo ""
    echo "계속 진행하시겠습니까? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Python API 서버 연결 확인됨"
fi

echo ""
echo "빌드 중..."
dotnet build --nologo

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ 빌드 실패"
    exit 1
fi

echo ""
echo "================================================"
echo "웹 애플리케이션 실행 중..."
echo "================================================"
echo ""
echo "✓ 아래 표시되는 URL로 브라우저에서 접속하세요."
echo ""
echo "중지하려면 Ctrl+C를 누르세요."
echo ""

dotnet run --no-build
