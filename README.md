# 261020_bucheon_huggingface_kmc

Hugging Face **Inference API**(`huggingface_hub.InferenceClient`)로 만든 **리뷰 감성 분석기**.
리뷰 텍스트를 입력하면 1~5점 별점과 확신도를 보여줍니다.

- 모델: [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) (한국어 포함 다국어)
- 모델을 내려받지 않고 원격 호출하므로 `torch`/`transformers`가 필요 없습니다.
- UI: Gradio

## 사전 준비

1. https://huggingface.co/settings/tokens 에서 토큰을 발급합니다 (Inference Providers 호출 권한 필요).
2. 아래 `.env`의 `HF_TOKEN`에 넣습니다.

## 설치

```bash
cd 261020_bucheon_hugging_kmc
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env       # macOS/Linux: cp .env.example .env
```

`.env`를 열어 `HF_TOKEN=hf_xxxxx` 로 채웁니다.

> Windows에서 경로가 길어 설치 중 `.pyc` 관련 오류가 나면 `pip install --no-compile -r requirements.txt` 를 사용하세요.

## 실행

```bash
python app.py
```

브라우저에서 http://127.0.0.1:7860 접속 → 리뷰를 **한 줄에 하나씩** 입력 후 Submit.
사용이 끝나면 화면 하단의 **서버 종료** 버튼으로 서버를 끌 수 있습니다 (터미널에서는 `Ctrl+C`).

## 환경변수 (`.env`)

| 변수 | 설명 | 기본값 |
|---|---|---|
| `HF_TOKEN` | Hugging Face 액세스 토큰 (**필수**) | - |
| `MODEL_NAME` | 호출할 모델 ID | `nlptown/bert-base-multilingual-uncased-sentiment` |

`.env`는 `.gitignore`로 제외되며, 공유용 템플릿은 `.env.example`입니다.

## 구조

```
README.md
261020_bucheon_hugging_kmc/
├─ app.py            Gradio 앱 (InferenceClient.text_classification 호출)
├─ requirements.txt  의존성
└─ .env.example      환경변수 템플릿
```
