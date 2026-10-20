import os
import threading

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "nlptown/bert-base-multilingual-uncased-sentiment")

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
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
    demo.launch()
