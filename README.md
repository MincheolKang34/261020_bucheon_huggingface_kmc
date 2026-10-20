# 261020_bucheon_huggingface_kmc

Hugging Face **Inference API**(`huggingface_hub.InferenceClient`)로 만든 **리뷰 감성 분석기**.
리뷰 텍스트를 입력하면 1~5점 별점과 확신도를 보여줍니다.

- 모델: [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) (한국어 포함 다국어)
- 모델을 내려받지 않고 원격 호출하므로 `torch`/`transformers`가 필요 없습니다.
- UI: Gradio

## 사전 준비

https://huggingface.co/settings/tokens 에서 토큰을 발급합니다 (Inference Providers 호출 권한 필요).
`.env`를 직접 편집할 필요는 없습니다. 처음 실행할 때 토큰이 없으면 앱이 입력을 요청합니다.

## 빠른 시작 (원클릭)

```bash
cd 261020_bucheon_hugging_kmc
run.bat          # Windows: 더블클릭도 가능
bash run.sh      # macOS/Linux, 또는 Windows의 Git Bash
```

`run.bat`(Windows) 또는 `run.sh` 하나로 **가상환경 생성 → 의존성 설치 → 앱 실행**까지 자동으로 진행합니다 .
처음 한 번만 설치 시간이 걸리고, 이후 실행은 빠릅니다. `HF_TOKEN`이 없으면 실행 중에 입력을 요청합니다.

## 수동 설치

```bash
cd 261020_bucheon_hugging_kmc
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

> Windows에서 경로가 길어 설치 중 `.pyc` 관련 오류가 나면 `pip install --no-compile -r requirements.txt` 를 사용하세요.

## 실행

가상환경(`venv`)을 활성화한 뒤 실행해야 합니다. 활성화하지 않고 `python app.py`만 실행하면 시스템 Python을 사용해 `gradio` 모듈을 찾지 못합니다.

```bash
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
python app.py
```

활성화 없이 한 번에 실행하려면 `venv\Scripts\python app.py` 또는 `run.bat`/`run.sh`를 사용하세요.

`HF_TOKEN`이 없으면 터미널에서 토큰 입력을 요청합니다. 붙여넣고 Enter를 누르면 유효성을 확인한 뒤 `.env`에 자동 저장하므로, 다음 실행부터는 묻지 않습니다 (잘못 입력하면 최대 3번까지 다시 입력).

브라우저에서 http://127.0.0.1:7860 접속 → 리뷰를 **한 줄에 하나씩** 입력 후 Submit.
사용이 끝나면 화면 하단의 **서버 종료** 버튼으로 서버를 끌 수 있습니다 (터미널에서는 `Ctrl+C`).

## 재시작

1. 서버가 켜져 있으면 먼저 끕니다 (화면의 **서버 종료** 버튼 또는 터미널에서 `Ctrl+C`).
2. `run.bat`(또는 `bash run.sh`)을 다시 실행합니다. 기존 `venv`를 재사용하므로 몇 초 안에 시작되고, 저장된 토큰은 다시 묻지 않습니다.
3. 설치 확인 없이 바로 켜려면 `venv\Scripts\python app.py` (macOS/Linux: `venv/bin/python app.py`).

이전 서버가 아직 켜져 있으면 포트 7860 사용 중 오류가 나므로 먼저 종료하세요.

## 환경변수 (`.env`)

| 변수 | 설명 | 기본값 |
|---|---|---|
| `HF_TOKEN` | Hugging Face 액세스 토큰 (없으면 실행 시 입력받아 자동 저장) | - |
| `MODEL_NAME` | 호출할 모델 ID | `nlptown/bert-base-multilingual-uncased-sentiment` |

`.env`는 `.gitignore`로 제외되며, 공유용 템플릿은 `.env.example`입니다.

## 구조

```
README.md
261020_bucheon_hugging_kmc/
├─ app.py            Gradio 앱 (InferenceClient.text_classification 호출)
├─ run.bat / run.sh  원클릭 실행 스크립트 (설치 + 실행)
├─ requirements.txt  의존성
└─ .env.example      환경변수 템플릿
```
