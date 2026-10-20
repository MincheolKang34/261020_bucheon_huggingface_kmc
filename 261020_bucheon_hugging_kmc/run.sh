#!/usr/bin/env bash
# 원클릭 실행: 가상환경 생성 -> 의존성 설치 -> 앱 실행
# 사용법: bash run.sh   (Windows는 Git Bash에서 실행)
set -e
cd "$(dirname "$0")"

export PYTHONIOENCODING=utf-8

# 실제로 실행되는 python 찾기 (Windows의 Microsoft Store 스텁은 건너뜀)
PY=""
for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys" >/dev/null 2>&1; then
        PY=$cand
        break
    fi
done
if [ -z "$PY" ]; then
    echo "[ERROR] Python이 설치되어 있지 않습니다. Python 3.8 이상을 설치하세요."
    exit 1
fi

# 가상환경 생성 (Windows: Scripts, macOS/Linux: bin)
if [ ! -d venv ]; then
    echo "[1/3] 가상환경 생성 중..."
    "$PY" -m venv venv
fi
if [ -x venv/Scripts/python.exe ]; then
    VENV_PY=venv/Scripts/python.exe
else
    VENV_PY=venv/bin/python
fi

echo "[2/3] 의존성 설치 중..."
# --no-compile: Windows 긴 경로에서 .pyc 생성 오류 방지
"$VENV_PY" -m pip install -q --no-compile -r requirements.txt

echo "[3/3] 앱 실행 (http://127.0.0.1:7860)"
exec "$VENV_PY" app.py
