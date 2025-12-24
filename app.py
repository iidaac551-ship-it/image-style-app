import streamlit as st
from PIL import Image
import base64
import io
import requests

# Gemini API 設定
API_KEY = "YOUR_GEMINI_API_KEY"
MODEL = "gemini-2.5-flash-image-preview"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Fashion Studio", layout="centered")

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "source_image" not in st.session_state:
    st.session_state.source_image = None
if "target_image" not in st.session_state:
    st.session_state.target_image = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "history" not in st.session_state:
    st.session_state.history = []
if "custom_request" not in st.session_state:
    st.session_state.custom_request = ""

# --- Helper Functions ---
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def call_gemini(prompt, source_img=None, target_img=None):
    parts = [{"text": prompt}]
    if source_img:
        parts.append({"inlineData": {"mimeType": "image/png", "data": image_to_base64(source_img)}})
    if target_img:
        parts.append({"inlineData": {"mimeType": "image/png", "data": image_to_base64(target_img)}})
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    response = requests.post(API_URL, json=payload)
    data = response.json()
    b64 = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("inlineData", {}).get("data")
    if b64:
        img_bytes = base64.b64decode(b64)
        return Image.open(io.BytesIO(img_bytes))
    return None

def undo():
    if st.session_state.history:
        st.session_state.current_image = st.session_state.history.pop()

# --- UI ---
st.title("🎨 Fashion Studio")

# ステップごとのヘッダー
steps_labels = [
    "アップロード", "服転送・生成", "画角・ポーズ", "髪型・髪色", 
    "表情", "ブランド・季節", "服の色・デザイン", "完成"
]
st.subheader(f"Step {st.session_state.step}: {steps_labels[st.session_state.step-1]}")

# --- Step 1: アップロード ---
if st.session_state.step == 1:
    source_file = st.file_uploader("モデル写真をアップロード", type=["png","jpg","jpeg"])
    if source_file:
        st.session_state.source_image = Image.open(source_file).convert("RGBA")
        st.session_state.current_image = st.session_state.source_image.copy()
        st.session_state.history = []
        st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 2))

# --- Step 2: 服転送 ---
elif st.session_state.step == 2:
    target_file = st.file_uploader("服装写真をアップロード", type=["png","jpg","jpeg"])
    st.text_area("リクエスト（服装を反映、顔は維持等）", value=st.session_state.custom_request, key="custom_request")
    if target_file:
        st.session_state.target_image = Image.open(target_file).convert("RGBA")
    if st.session_state.current_image:
        st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
        if st.button("生成"):
            st.session_state.history.append(st.session_state.current_image.copy())
            prompt = f"Transfer outfit from image 2 to image 1. Keep face as is. {st.session_state.custom_request}"
            result = call_gemini(prompt, source_img=st.session_state.source_image, target_img=st.session_state.target_image)
            if result:
                st.session_state.current_image = result
            st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 3))
    st.button("Undo", on_click=undo)

# --- Step 3: 画角・ポーズ ---
elif st.session_state.step == 3:
    st.text_area("リクエスト（ポーズや角度の希望）", value=st.session_state.custom_request, key="custom_request")
    angles = ["正面","斜め45度","真横","ハイアングル","ローアングル","自撮り風","アップ","俯瞰"]*10
    poses = st.multiselect("ポーズ選択", angles)
    st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
    if st.button("生成"):
        st.session_state.history.append(st.session_state.current_image.copy())
        prompt = f"Change pose/angle: {poses}. Keep face. {st.session_state.custom_request}"
        result = call_gemini(prompt, source_img=st.session_state.current_image)
        if result:
            st.session_state.current_image = result
    st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 4))
    st.button("Undo", on_click=undo)

# --- Step 4: 髪型・髪色 ---
elif st.session_state.step == 4:
    st.text_area("リクエスト（髪型・髪色）", value=st.session_state.custom_request, key="custom_request")
    hairs = ["ショートボブ","ロング","ポニーテール","お団子"]*12
    hair_colors = ["黒","茶","金","赤","青","ピンク"]*8
    hair_sel = st.selectbox("髪型選択", hairs)
    color_sel = st.selectbox("髪色選択", hair_colors)
    st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
    if st.button("生成"):
        st.session_state.history.append(st.session_state.current_image.copy())
        prompt = f"Change hair to {hair_sel} with color {color_sel}. Keep face and pose. {st.session_state.custom_request}"
        result = call_gemini(prompt, source_img=st.session_state.current_image)
        if result:
            st.session_state.current_image = result
    st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 5))
    st.button("Undo", on_click=undo)

# --- Step 5: 表情 ---
elif st.session_state.step == 5:
    st.text_area("リクエスト（表情）", value=st.session_state.custom_request, key="custom_request")
    expressions = ["自然体","微笑み","笑顔","クール","自信","アンニュイ"]*10
    exp_sel = st.selectbox("表情選択", expressions)
    st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
    if st.button("生成"):
        st.session_state.history.append(st.session_state.current_image.copy())
        prompt = f"Change facial expression to {exp_sel}. Keep other features. {st.session_state.custom_request}"
        result = call_gemini(prompt, source_img=st.session_state.current_image)
        if result:
            st.session_state.current_image = result
    st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 6))
    st.button("Undo", on_click=undo)

# --- Step 6: ブランド・季節 ---
elif st.session_state.step == 6:
    st.text_area("リクエスト（ブランド・季節）", value=st.session_state.custom_request, key="custom_request")
    brands = ["CHANEL","DIOR","GUCCI","PRADA","LOUIS VUITTON","CELINE"]*16
    seasons = ["春","夏","秋","冬"]
    brand_sel = st.selectbox("ブランド選択", brands)
    season_sel = st.selectbox("季節選択", seasons)
    st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
    if st.button("生成"):
        st.session_state.history.append(st.session_state.current_image.copy())
        prompt = f"Infuse style of {brand_sel} {season_sel}. Keep face and pose. {st.session_state.custom_request}"
        result = call_gemini(prompt, source_img=st.session_state.current_image)
        if result:
            st.session_state.current_image = result
    st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 7))
    st.button("Undo", on_click=undo)

# --- Step 7: 服の色・デザイン ---
elif st.session_state.step == 7:
    st.text_area("リクエスト（服の色・デザイン）", value=st.session_state.custom_request, key="custom_request")
    colors = ["オリジナル","白","黒","ピンク","青","ラベンダー"]*10
    color_sel = st.selectbox("服色選択", colors)
    st.image(st.session_state.current_image, caption="プレビュー", use_column_width=True)
    if st.button("生成"):
        st.session_state.history.append(st.session_state.current_image.copy())
        prompt = f"Change clothing color/design to {color_sel}. Keep face, pose, hair. {st.session_state.custom_request}"
        result = call_gemini(prompt, source_img=st.session_state.current_image)
        if result:
            st.session_state.current_image = result
    st.button("次へ", on_click=lambda: st.session_state.__setitem__("step", 8))
    st.button("Undo", on_click=undo)

# --- Step 8: 完成 ---
elif st.session_state.step == 8:
    st.subheader("✨ 完成画像")
    st.image(st.session_state.current_image, caption="完成画像", use_column_width=True)
    buf = io.BytesIO()
    st.session_state.current_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("Download PNG", data=byte_im, file_name="fashion_studio.png", mime="image/png")
    st.button("Restart", on_click=lambda: st.session_state.__setitem__("step", 1))

