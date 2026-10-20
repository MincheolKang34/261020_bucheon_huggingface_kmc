import getpass
import os
import threading

import gradio as gr
from dotenv import load_dotenv, set_key
from huggingface_hub import InferenceClient, whoami

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(ENV_PATH)
MODEL_NAME = os.getenv("MODEL_NAME", "nlptown/bert-base-multilingual-uncased-sentiment")


def ensure_token(env_path=ENV_PATH, max_tries=3):
    """HF_TOKEN이 없으면 입력받아 검증한 뒤 .env에 저장하고, 있으면 그대로 사용."""
    token = os.getenv("HF_TOKEN", "").strip()
    if token:
        return token
    print("HF_TOKEN이 설정되어 있지 않습니다.")
    print("https://huggingface.co/settings/tokens 에서 토큰을 발급받아 붙여넣으세요.")
    for _ in range(max_tries):
        token = getpass.getpass("HF_TOKEN (입력 내용은 화면에 표시되지 않습니다): ").strip()
        try:
            whoami(token=token)
        except Exception:
            print("유효하지 않은 토큰입니다. 다시 입력해 주세요.")
            continue
        set_key(env_path, "HF_TOKEN", token)
        os.environ["HF_TOKEN"] = token
        print(f"토큰을 확인하고 {os.path.basename(env_path)}에 저장했습니다.")
        return token
    raise SystemExit("토큰 입력에 실패했습니다. 토큰을 확인한 뒤 다시 실행해 주세요.")


client = InferenceClient(
    provider="hf-inference",
    api_key=ensure_token(),
)


def analyze(text):
    """줄마다 별점(1~5)과 확신도를 계산해 표로 반환."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    rows = []
    for line in lines:
        # 반환: label이 "1 star" ~ "5 stars"인 후보 목록 (확신도 내림차순)
        top = client.text_classification(line, model=MODEL_NAME)[0]
        stars = int(top.label.split()[0])
        rows.append([line, "⭐" * stars, stars, round(top.score, 3)])
    return rows


review_ui = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(lines=6, label="리뷰 입력 (한 줄에 리뷰 하나)"),
    outputs=gr.Dataframe(headers=["리뷰", "별점", "점수(1~5)", "확신도"], label="결과"),
    title="리뷰 감성 분석기",
    description=f"모델: {MODEL_NAME} (Hugging Face Inference API)",
    examples=[["배송도 빠르고 품질도 훌륭해요!\n너무 실망스럽고 다시는 안 살 거예요."]],
    allow_flagging="never",
)


def shutdown():
    """응답을 돌려준 뒤 프로세스를 종료."""
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return "서버를 종료합니다. 이 탭을 닫아도 됩니다."


with gr.Blocks() as demo:
    review_ui.render()
    stop_btn = gr.Button("서버 종료", variant="stop")
    stop_msg = gr.Markdown()
    stop_btn.click(shutdown, outputs=stop_msg)

if __name__ == "__main__":
    demo.launch(inbrowser=True)  # 실행하면 브라우저를 자동으로 연다
