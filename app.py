import streamlit as st
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Fashion Studio", layout="centered")
st.title("🎨 Fashion Studio")

# -----------------------------
# セッションステート初期化
# -----------------------------
if 'step' not in st.session_state:
    st.session_state.step = 2
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# -----------------------------
# 画像アップロード
# -----------------------------
source_file = st.file_uploader("モデル写真をアップロード", type=['png','jpg','jpeg'], key='source')
target_file = st.file_uploader("服装写真をアップロード", type=['png','jpg','jpeg'], key='target')

def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def save_history(img):
    if img:
        st.session_state.history.append(img)

# モデル画像
if source_file:
    source_img = Image.open(source_file)
    st.session_state.current_image = source_img
    st.image(source_img, caption="モデル画像", use_column_width=True)

# 服装画像
if target_file:
    target_img = Image.open(target_file)
    st.image(target_img, caption="服装画像", use_column_width=True)

# -----------------------------
# Undo機能
# -----------------------------
if st.button("一つ戻る"):
    if st.session_state.history:
        st.session_state.current_image = st.session_state.history.pop()
    if st.session_state.step > 2:
        st.session_state.step -= 1

# -----------------------------
# ステップ3: 画角・ポーズ
# -----------------------------
if st.session_state.step == 3:
    st.subheader("画角・ポーズ")
    pose_options = [f"ポーズ{i+1}" for i in range(80)]
    selected_pose = st.selectbox("ポーズを選択", pose_options)
    if st.button("次へ"):
        st.session_state.step += 1

# -----------------------------
# ステップ4: 髪型・髪色
# -----------------------------
if st.session_state.step == 4:
    st.subheader("髪型・髪色")
    hair_options = [f"髪型{i+1}" for i in range(50)]
    hair_color_options = ["黒","茶","金","赤","青","紫","ピンク"]
    selected_hair = st.selectbox("髪型を選択", hair_options)
    selected_color = st.selectbox("髪色を選択", hair_color_options)
    if st.button("次へ"):
        st.session_state.step += 1

# -----------------------------
# ステップ5: 表情
# -----------------------------
if st.session_state.step == 5:
    st.subheader("表情")
    expression_options = ["自然体","笑顔","微笑み","クール","自信","アンニュイ"]
    selected_expression = st.selectbox("表情を選択", expression_options)
    if st.button("次へ"):
        st.session_state.step += 1

# -----------------------------
# ステップ6: ブランド・季節
# -----------------------------
if st.session_state.step == 6:
    st.subheader("ブランド・季節")
    brand_options = [f"ブランド{i+1}" for i in range(100)]
    selected_brand = st.selectbox("ブランドを選択", brand_options)
    season_options = ["春","夏","秋","冬"]
    selected_season = st.selectbox("季節を選択", season_options)
    if st.button("次へ"):
        st.session_state.step += 1

# -----------------------------
# ステップ7: 服の色・デザイン
# -----------------------------
if st.session_state.step == 7:
    st.subheader("服の色・デザイン")
    clothing_colors = ["赤","青","黒","白","ピンク","黄色","緑","オリジナル"]
    selected_clothing = st.selectbox("服の色を選択", clothing_colors)
    if st.button("生成する"):
        st.success("ここでAI生成処理を呼び出します。")
        # 例:
        # st.session_state.current_image = call_gemini_api(source_img, target_img, selected_pose, selected_hair, selected_color, selected_expression, selected_brand, selected_season, selected_clothing, magic_request)

# -----------------------------
# Magic Request（自由入力）
# -----------------------------
magic_request = st.text_area("Magic Request（自由リクエスト）", placeholder="例：背景を明るく、顔はそのまま...")

# -----------------------------
# プレビュー表示
# -----------------------------
if st.session_state.current_image:
    st.subheader("プレビュー")
    st.image(st.session_state.current_image, use_column_width=True)
