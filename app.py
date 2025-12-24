# app.py
import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="Fashion Style Studio", layout="wide")

# --- 初期状態 ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "source_img" not in st.session_state:
    st.session_state.source_img = None
if "target_img" not in st.session_state:
    st.session_state.target_img = None
if "current_img" not in st.session_state:
    st.session_state.current_img = None
if "history" not in st.session_state:
    st.session_state.history = []

# --- ユーザー選択肢 ---
angle_options = [f"角度{i}" for i in range(1, 81)]  # 80パターン
pose_options = [f"ポーズ{i}" for i in range(1, 81)]
hair_options = [f"髪型{i}" for i in range(1, 51)]
hair_color_options = ["黒", "茶", "金", "赤", "ピンク", "青", "緑"]
expression_options = ["自然体", "笑顔", "クール", "微笑み"]
brand_options = [f"ブランド{i}" for i in range(1, 101)]
season_options = ["春", "夏", "秋", "冬"]
cloth_color_options = ["赤", "青", "緑", "黄", "白", "黒"]

# --- ヘルパー関数 ---
def load_image(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGBA")
        return img
    return None

def add_history(img):
    if img is not None:
        st.session_state.history.append(img.copy())

# --- UI ---
st.title("🎨 Fashion Style Studio")

# ステップ表示
st.subheader(f"ステップ {st.session_state.step}")

# 画像表示
if st.session_state.current_img:
    st.image(st.session_state.current_img, width=300)
else:
    st.text("画像をアップロードしてください")

# Undo ボタン
if st.session_state.history:
    if st.button("← 1つ戻す（画像）"):
        st.session_state.current_img = st.session_state.history.pop()

# --- ステップごとの処理 ---
if st.session_state.step == 1:
    uploaded = st.file_uploader("モデル写真をアップロード", type=["png", "jpg", "jpeg"])
    if uploaded:
        img = load_image(uploaded)
        st.session_state.source_img = img
        st.session_state.current_img = img.copy()
        st.session_state.history = []
        st.button("生成開始", on_click=lambda: st.session_state.update(step=2))

elif st.session_state.step == 2:
    uploaded = st.file_uploader("服装画像をアップロード（顔や背景は使わない）", type=["png", "jpg", "jpeg"])
    if uploaded:
        img = load_image(uploaded)
        st.session_state.target_img = img
        st.button("服装適用", on_click=lambda: st.session_state.update(step=3))

elif st.session_state.step == 3:
    angle = st.selectbox("画角・角度を選択", angle_options)
    pose = st.selectbox("ポーズを選択", pose_options)
    custom_req = st.text_input("追加リクエスト（任意）")
    if st.button("生成"):
        add_history(st.session_state.current_img)
        # --- AI処理の代替としてここでは画像をそのままコピー ---
        st.session_state.current_img = st.session_state.current_img.copy()
        st.session_state.step += 1

elif st.session_state.step == 4:
    hair = st.selectbox("髪型を選択", hair_options)
    hair_color = st.selectbox("髪色を選択", hair_color_options)
    custom_req = st.text_input("追加リクエスト（任意）")
    if st.button("生成"):
        add_history(st.session_state.current_img)
        st.session_state.current_img = st.session_state.current_img.copy()
        st.session_state.step += 1

elif st.session_state.step == 5:
    expression = st.selectbox("表情を選択", expression_options)
    custom_req = st.text_input("追加リクエスト（任意）")
    if st.button("生成"):
        add_history(st.session_state.current_img)
        st.session_state.current_img = st.session_state.current_img.copy()
        st.session_state.step += 1

elif st.session_state.step == 6:
    brand = st.selectbox("ブランドを選択", brand_options)
    season = st.selectbox("季節を選択", season_options)
    custom_req = st.text_input("追加リクエスト（任意）")
    if st.button("生成"):
        add_history(st.session_state.current_img)
        st.session_state.current_img = st.session_state.current_img.copy()
        st.session_state.step += 1

elif st.session_state.step == 7:
    cloth_color = st.selectbox("服の色を選択", cloth_color_options)
    custom_req = st.text_input("追加リクエスト（任意）")
    if st.button("生成"):
        add_history(st.session_state.current_img)
        st.session_state.current_img = st.session_state.current_img.copy()
        st.session_state.step += 1

# --- 最終画像ダウンロード ---
if st.session_state.step > 7:
    st.success("最終画像完成！")
    buf = io.BytesIO()
    st.session_state.current_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    b64 = base64.b64encode(byte_im).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="fashion_studio.png">💾 画像を保存</a>'
    st.markdown(href, unsafe_allow_html=True)
